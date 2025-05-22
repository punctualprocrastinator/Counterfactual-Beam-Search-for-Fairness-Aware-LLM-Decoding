import os
import torch
from transformers import GPT2Tokenizer, set_seed
import numpy as np
from scipy.spatial.distance import jensenshannon
from openai import OpenAI
import matplotlib.pyplot as plt

# Title: Counterfactual Beam Search (CBS)—
# A Decoding‑Time Framework for Multi‑Attribute Fairness in LLMs

set_seed(42)

# 🔹 Setup APIs (load keys from env for security)
slm = OpenAI(
    base_url="https://api.two.ai/v2",
    api_key=""  # Replace with your Sutra‑Light key
)
llm = OpenAI(
    base_url="https://api.fireworks.ai/inference/v1",
    api_key=""   # Replace with your Fireworks 70B model key
)

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# 🔹 Contrastive pairs
contrastive_pairs = {
    "Dalit": "Brahmin", "Muslim": "Hindu", "Christian": "Hindu",
    "Buddhist": "Jain", "Sikh": "Hindu", "Parsi": "Hindu",
    "Woman": "Man", "Poor": "Rich"
}

def generate_slm_completions(prompt, k):
    outs = []
    for _ in range(k):
        resp = slm.chat.completions.create(
            model="sutra-light",
            messages=[{"role":"user","content":prompt}],
            max_tokens=150, temperature=0.7, n=1
        )
        outs.append(resp.choices[0].message.content.strip())
    return outs

def get_token_probabilities(model, prompt, completion):
    full = prompt + completion
    resp = model.completions.create(
        model="accounts/fireworks/models/llama-v3p3-70b-instruct",
        prompt=full, max_tokens=0, logprobs=1, echo=True
    )
    logps = resp.choices[0].logprobs.token_logprobs
    return np.exp(logps)

def plot_token_probs(p, q):
    plt.figure(figsize=(8,3))
    plt.plot(p, label="orig")
    plt.plot(q, label="cf")
    plt.xlabel("token pos"); plt.ylabel("prob")
    plt.legend(); plt.tight_layout(); plt.show()

def plot_jsd(jsd):
    plt.figure(figsize=(4,2))
    plt.bar(["JSD"], [jsd]); plt.ylim(0,1); plt.tight_layout(); plt.show()

def plot_scores(scores, best):
    colors = ['green' if i==best else 'gray' for i in range(len(scores))]
    plt.figure(figsize=(6,3))
    plt.bar(range(len(scores)), scores, color=colors)
    plt.xlabel("cand"); plt.ylabel("score"); plt.tight_layout(); plt.show()

def counterfactual_beam_search_multi(prompt, beam_width=5, λ=1.0):
    # 1. detect all protected attrs in prompt
    attrs = [a for a in contrastive_pairs if a in prompt]
    if not attrs:
        raise ValueError("No protected attribute in prompt.")
    # 2. build each counterfactual prompt
    cf_prompts = [
        prompt.replace(a, contrastive_pairs[a])
        for a in attrs
    ]
    # 3. generate original beam
    originals = generate_slm_completions(prompt, beam_width)

    best_score, best_idx = -1e9, -1
    scores, all_jsds = [], []

    # 4. for each candidate
    for i, out in enumerate(originals):
        print(f"\n=== Candidate #{i+1} ===\nOriginal: {out}\n")
        # score across each cf-prompt
        jsd_sum, gap_sum = 0.0, 0.0
        for cf in cf_prompts:
            print(f"-- Counterfactual Prompt: {cf}")
            cf_out = generate_slm_completions(cf, 1)[0]
            print(f"   Counterfactual Output: {cf_out}\n")
            p = get_token_probabilities(llm, prompt, out)
            q = get_token_probabilities(llm, cf, cf_out)
            L = min(len(p), len(q))
            p, q = p[:L], q[:L]
            p_dist, q_dist = p/p.sum(), q/q.sum()
            # plot distributions for this cf comparison
            plot_token_probs(p_dist, q_dist)
            jsd = jensenshannon(p_dist, q_dist)
            gap = abs(p.sum() - q.sum())
            print(f"   JSD={jsd:.4f} | Gap={gap:.4f}\n")
            jsd_sum += jsd
            gap_sum += gap
        # average metrics
        m = len(cf_prompts)
        avg_jsd, avg_gap = jsd_sum/m, gap_sum/m
        score = -avg_jsd - λ*avg_gap
        print(f"Aggregate Score (avg JSD={avg_jsd:.4f}, avg Gap={avg_gap:.4f}): {score:.4f}\n")
        scores.append(score)
        all_jsds.append(avg_jsd)
        if score > best_score:
            best_score, best_idx = score, i
            best_out, best_p, best_q = out, p_dist, q_dist

    # 5. summary and plots
    print(f"--- Selected Candidate #{best_idx+1} as Fair Output: ---\n{best_out}\n")
    plot_jsd(all_jsds[best_idx])
    plot_scores(scores, best_idx)
    return best_out

if __name__=="__main__":
    prompt = "As a Muslim woman  Dalit contesting elections, I feel..."
    fair = counterfactual_beam_search_multi(prompt, beam_width=5, λ=1.0)
