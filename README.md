
# Counterfactual-Beam-Search-for-Fairness-Aware-LLM-Decoding
Large language models (LLMs) can inadvertently amplify social biases tied to protected attributes (e.g. religion, gender). We propose Counterfactual Beam Search (CBS), a decoding‑time reranking method that selects the candidate continuation whose token‑probability distribution is least sensitive to swapping a protected attribute with its counterfactual. We quantify sensitivity via Jensen–Shannon divergence (JSD) and likelihood gap, and extend the scoring with axis‑wise normalization and temperature scaling. We evaluate on two axes (religion: Muslim↔Hindu; gender pronouns: he↔she).
# EXAMPLE 
=== Candidate #1 ===
As a Muslim contesting elections, you may feel a range of emotions and thoughts. It's common to experience a mix of pride, responsibility, and perhaps some anxiety. You might feel a strong sense of duty to represent your community and address their concerns, while also navigating the challenges that come with political campaigning.

You may consider how your identity influences your platform and the issues you choose to prioritize, such as social justice, equality, and community welfare. Additionally, you might reflect on the importance of fostering understanding and dialogue among diverse groups in society, promoting inclusivity, and combating stereotypes or misconceptions about your faith.

Facing scrutiny or bias can also be a concern, so preparing to address these challenges with confidence and grace is important. Building a supportive network within your


JSD=0.4140 | Likelihood Gap=2.4579 | Score=-2.8719

=== Candidate #2 ===
It's important to acknowledge that contesting elections as a Muslim can bring a unique set of experiences and challenges. You may feel a mix of pride, responsibility, and perhaps even apprehension. 

Pride can stem from the opportunity to represent your community and uphold values that are important to you and your constituents. Responsibility arises from the understanding that your actions and decisions could significantly impact your community's representation and well-being. 

Challenges might include navigating stereotypes or biases, addressing concerns about how your faith influences your political views, and working to build bridges among diverse groups of voters. Engaging in open dialogue and promoting understanding can be crucial for fostering a positive campaign environment.

Ultimately, your commitment to serving the public and advocating for inclusive policies can resonate with a wide array


JSD=0.4294 | Likelihood Gap=5.4933 | Score=-5.9226

=== Candidate #3 ===
As a Muslim contesting elections, you might feel a range of emotions and thoughts. You may experience a sense of responsibility to represent your community and address their concerns. There could be a mix of pride and apprehension about navigating the political landscape, especially in contexts where your faith may influence public perception.

You might also consider the importance of promoting inclusivity and understanding among diverse groups while advocating for policies that reflect your values and those of your constituents. Additionally, you may face challenges related to stereotypes or biases, which could impact your campaign and interactions with voters. 

Ultimately, your experience will be shaped by your personal beliefs, the political environment, and the specific issues at stake in your election. Engaging with your community and focusing on shared values can help


JSD=0.3330 | Likelihood Gap=0.1190 | Score=-0.4520

=== Candidate #4 ===
As a Muslim contesting elections, you may feel a mix of emotions, including pride, responsibility, and perhaps some apprehension. Pride comes from the opportunity to represent your community and contribute to the democratic process. Responsibility arises from the desire to address the needs and concerns of your constituents while upholding your values and beliefs. 

You might also face challenges, such as navigating public perceptions, addressing potential biases, and ensuring that your platform resonates with a diverse electorate. Engaging with various communities, promoting inclusivity, and focusing on common issues can help you connect with a broader audience. Ultimately, your commitment to serving the public good can be a strong motivator as you embark on this journey.


JSD=0.3749 | Likelihood Gap=15.0952 | Score=-15.4701

=== Candidate #5 ===
As a Muslim contesting elections, you may feel a mix of emotions ranging from hope and determination to apprehension and concern. Navigating the electoral landscape can be challenging, especially when considering factors such as public perception, community support, and the potential for discrimination or bias. 

You might be motivated by a desire to represent your community's interests, advocate for social justice, and promote policies that align with your values and beliefs. Engaging with constituents, addressing their concerns, and fostering inclusivity can be essential aspects of your campaign. 

At the same time, it's important to be aware of the broader political climate and how it may affect your candidacy. Building coalitions with diverse groups and emphasizing shared values can help create a more inclusive platform that resonates


JSD=0.4297 | Likelihood Gap=6.4000 | Score=-6.8297

--- Selected Fair Output ---
As a Muslim contesting elections, you might feel a range of emotions and thoughts. You may experience a sense of responsibility to represent your community and address their concerns. There could be a mix of pride and apprehension about navigating the political landscape, especially in contexts where your faith may influence public perception.

You might also consider the importance of promoting inclusivity and understanding among diverse groups while advocating for policies that reflect your values and those of your constituents. Additionally, you may face challenges related to stereotypes or biases, which could impact your campaign and interactions with voters. 

Ultimately, your experience will be shaped by your personal beliefs, the political environment, and the specific issues at stake in your election. Engaging with your community and focusing on shared values can help

Top 10 tokens with biggest probability shift:
     Ġpolicies   p=0.0138   q=0.0000   Δ=0.0138
           Ġin   p=0.0138   q=0.0001   Δ=0.0137
             Ċ   p=0.0001   q=0.0138   Δ=0.0136
          Ġthe   p=0.0001   q=0.0138   Δ=0.0136
       Ġbiases   p=0.0138   q=0.0003   Δ=0.0135
           Ġor   p=0.0004   q=0.0138   Δ=0.0134
           Ġbe   p=0.0006   q=0.0138   Δ=0.0132
         Ġyour   p=0.0138   q=0.0006   Δ=0.0132
      Ġrelated   p=0.0137   q=0.0005   Δ=0.0132
     Ġconsider   p=0.0002   q=0.0132   Δ=0.0130

Top 10 tokens most consistently treated:
           ing   p=0.0000   q=0.0000   Δ=0.0000
            Ġa   p=0.0001   q=0.0001   Δ=0.0000
          Ġmay   p=0.0000   q=0.0000   Δ=0.0000
        Ġrange   p=0.0000   q=0.0000   Δ=0.0000
            Ġa   p=0.0000   q=0.0000   Δ=0.0000
      Ġcontest   p=0.0000   q=0.0000   Δ=0.0000
        ĠThere   p=0.0138   q=0.0138   Δ=0.0000
       ĠMuslim   p=0.0003   q=0.0003   Δ=0.0000
           Ġof   p=0.0138   q=0.0137   Δ=0.0000
     Ġthoughts   p=0.0138   q=0.0138   Δ=0.0000

