# Todo
- [X] Import the exid data
- [X] 4 Param Model
- [X] 2 Param Model
- [X] New model for the sample interaction dataset of baris
- [ ] implement old models for comparison
- [ ] train the model on baris data 
- [ ] test baris data on multiple scenarios
- [ ] Visualizations of findings
- [ ] presentation 

Frage:
For the target vector y, do I take the difference of the acceleration or the acceleration of the second/first car?

relative distance x/y
relative velocity
relative acceleration 
acceleration should 

# Concept presentation
## Problem statement
## Brief description of the proposed method and concept
## Discussion about challenges regarding the implementation
## Timetable with milestones

- idea of social ai for cars
- concept of analyzing the behaviour of cars in relation to each other
- hope is to be able to predict the motion and behaviour of cars in different conditions more accuratly by explaining their interaction with each other
- similiar concepts were done in the following papers
  - Who are you with and Where are you going?  (Kota Yamaguchi , Alexander C. Berg , Luis E. Ortiz)
  - TOOD: Summar of what they are doing 


# Final presentation 
## Motivation and problem statement
## Detailed description of the implemented method
## Advantages and disadvantages of the implementation
## Evaluation of the results

# Report 
## Problem statement
## Concept overview
## Description of the proposed method and the implementation
## Evaluation of the results (≥ three different scenarios)
## Conclusions and future work


# Code (Every criteria fullfilled)
Structure (modularity, maintainability, avoidance of deep nesting and hard coded parameters, cleanness,...)
Documentation (meaningful comments, README file, ...)ris
Formatting (consistent indentation, compliance with PEP8, ...)
Runtime should be considered, but is not the main evaluation criterion.



# Baris
- exiting lane
- entering lane
- detecting the car pair


recording id

array 
frame numbers
id of the cars

whether exiting 
or entering



# Gpt prompts


Help me with creating content for a presentation using this content overview:
- Motivation and problem statement
- Detailed description of the implemented method
- Advantages and disadvantages of the implementation
- Evaluation of the results

Now I will give you all the information for the course we have

Title of our course: Scene-aware and Social-aware Motion Prediction for Autonomous Driving
Introduction and background:
Understanding motion behavior of human-driven vehicles is critical for
attaining safety of autonomous driving. This prediction is challenging
because human motion is inherently multimodal and scene-dependent [1]

Social acceptance is crucial in prediction. Some trajectories are physically
possible but socially unacceptable. Human drivers typically respect social
norms like yielding right-of-way or respecting personal space.

In recent years, tools from social-aware artificial intelligence (AI) have
been used to predict the behaviour of humans and human drivers [2] [3]

Problem: these tools work well, but are not control-oriented! (no system
model, no easy interpretation for the intents of interacting agents)

Our goal:
1) Test and evaluate state of the art
Test some of these social-aware AI tools (e.g. SVG-net);
Apply to relevant CommonRoad scenarios;
Consider different scenarios: curved roads, intersections, etc;
Sensitivity analysis (i.e. generalization capabilities);
...
2) New control-oriented (interpretable) tools
Use Kalman prediction as the basic framework;
Scene context: incorporate constraints;
Multi-agent context: cooperative prediction (information sharing);
Multi-modal context: include virtual forces among agents;

In our group we only focused on the 
- Consider different scenarios curved roads, intersections, etc;
- Multi-modal context: include virtual forces among agents;


These are the paper abstracts that were given to us.

Title: Social LSTM - Human Trajectory Prediction in Crowded Spaces
Abstract:
Pedestrians follow different trajectories to avoid obsta-
cles and accommodate fellow pedestrians. Any autonomous
vehicle navigating such a scene should be able to foresee
the future positions of pedestrians and accordingly adjust
its path to avoid collisions. This problem of trajectory pre-
diction can be viewed as a sequence generation task, where
we are interested in predicting the future trajectory of peo-
ple based on their past positions. Following the recent suc-
cess of Recurrent Neural Network (RNN) models for se-
quence prediction tasks, we propose an LSTM model which
can learn general human movement and predict their future
trajectories. This is in contrast to traditional approaches
which use hand-crafted functions such as Social forces. We
demonstrate the performance of our method on several pub-
lic datasets. Our model outperforms state-of-the-art meth-
ods on some of these datasets . We also analyze the tra-
jectories predicted by our model to demonstrate the motion
behaviour learned by our model.

Title: Who are you with and Where are you going?
Abstract:
We propose an agent-based behavioral model of pedes-
trians to improve tracking performance in realistic scenar-
ios. In this model, we view pedestrians as decision-making
agents who consider a plethora of personal, social, and en-
vironmental factors to decide where to go next. We formu-
late prediction of pedestrian behavior as an energy mini-
mization on this model. Two of our main contributions are
simple, yet effective estimates of pedestrian destination and
social relationships (groups). Our final contribution is to
incorporate these hidden properties into an energy formu-
lation that results in accurate behavioral prediction. We
evaluate both our estimates of destination and grouping,
as well as our accuracy at prediction and tracking against
state of the art behavioral model and show improvements,
especially in the challenging observational situation of in-
frequent appearance observations – something that might
occur in thousands of webcams available on the Internet.

Title: Social GAN -  Socially Acceptable Trajectories with Generative Adversarial Networks
Abstract:
Understanding human motion behavior is critical for au-
tonomous moving platforms (like self-driving cars and so-
cial robots) if they are to navigate human-centric environ-
ments. This is challenging because human motion is inher-
ently multimodal: given a history of human motion paths,
there are many socially plausible ways that people could
move in the future. We tackle this problem by combining
tools from sequence prediction and generative adversar-
ial networks: a recurrent sequence-to-sequence model ob-
serves motion histories and predicts future behavior, using
a novel pooling mechanism to aggregate information across
people. We predict socially plausible futures by training ad-
versarially against a recurrent discriminator, and encour-
age diverse predictions with a novel variety loss. Through
experiments on several datasets we demonstrate that our
approach outperforms prior work in terms of accuracy, va-
riety, collision avoidance, and computational complexity.


Title: Human Trajectory Forecasting in Crowds - A Deep Learning Perspective
Abstract: 
Since the past few decades, human trajectory fore-
casting has been a field of active research owing to its nu-
merous real-world applications: evacuation situation analysis,
deployment of intelligent transport systems, traffic operations, to
name a few. Early works handcrafted this representation based
on domain knowledge. However, social interactions in crowded
environments are not only diverse but often subtle. Recently,
deep learning methods have outperformed their handcrafted
counterparts, as they learned about human-human interactions
in a more generic data-driven fashion. In this work, we present
an in-depth analysis of existing deep learning-based methods
for modelling social interactions. We propose two knowledge-
based data-driven methods to effectively capture these social
interactions. To objectively compare the performance of these
interaction-based forecasting models, we develop a large scale
interaction-centric benchmark TrajNet++, a significant yet miss-
ing component in the field of human trajectory forecasting. We
propose novel performance metrics that evaluate the ability of
a model to output socially acceptable trajectories. Experiments
on TrajNet++ validate the need for our proposed metrics, and
our method outperforms competitive baselines on both real-world
and synthetic datasets.

**Answer**
Great, you have a solid foundation for your presentation. Let's organize the content for each section of your presentation:
1. Motivation and Problem Statement:

    Introduction to Autonomous Driving and Motion Prediction:
        Briefly explain the importance of understanding human-driven vehicle motion for autonomous driving safety.
        Highlight the challenges of predicting human motion due to its multimodal and scene-dependent nature.
        Emphasize the significance of social acceptance in motion prediction, considering social norms for safe and acceptable behavior.

2. Detailed Description of the Implemented Method:
2.1. Existing Social-aware AI Tools:

    Overview of Social LSTM:
        Explain the trajectory prediction problem in crowded spaces.
        Introduce the Social LSTM model as a solution, emphasizing its use of LSTM for sequence prediction.
        Discuss the contrast with traditional approaches like Social forces.

    Agent-based Behavioral Model:
        Introduce the agent-based model proposed in "Who are you with and Where are you going?"
        Explain how this model views pedestrians as decision-making agents considering personal, social, and environmental factors.
        Highlight contributions, including estimates of destination and social relationships.

    Social GAN for Socially Acceptable Trajectories:
        Describe the challenge of understanding human motion behavior in human-centric environments.
        Present the Social GAN approach, combining sequence prediction and generative adversarial networks.
        Discuss the novel pooling mechanism, adversarial training, and variety loss for predicting socially plausible futures.

    Deep Learning Perspective on Human Trajectory Forecasting:
        Provide an overview of the shift from handcrafted representations to data-driven deep learning methods.
        Introduce the deep learning-based methods for modeling social interactions discussed in "Human Trajectory Forecasting in Crowds."

2.2. Group's Focus:

    Test and Evaluation:
        Explain the goal of testing and evaluating state-of-the-art social-aware AI tools, using scenarios such as curved roads and intersections.
        Mention the focus on multi-modal context, specifically incorporating virtual forces among agents.

3. Advantages and Disadvantages of the Implementation:

    Advantages:
        Discuss the improved prediction capabilities demonstrated by Social LSTM, agent-based models, Social GAN, and deep learning methods.
        Emphasize the interpretability and control-oriented nature of the new tools proposed by the group.

    Disadvantages:
        Acknowledge potential limitations, such as computational complexity, dataset dependencies, or challenges in certain scenarios.
        Discuss any trade-offs made in the implementation process.

4. Evaluation of the Results:

    Comparison with State-of-the-Art:
        Present comparative results of the implemented methods against state-of-the-art approaches.
        Highlight performance metrics, accuracy, collision avoidance, and computational complexity.

    Addressing Challenges and Future Work:
        Discuss how the implemented methods addressed challenges in curved roads, intersections, and multi-modal scenarios.
        Mention potential areas for improvement and future research directions.

Conclusion:

    Summarize Key Findings:
        Recap the key findings and contributions of the implemented methods.
        Emphasize the importance of interpretable, control-oriented tools for autonomous driving.

    Closing Remarks:
        Conclude by reiterating the significance of scene-aware and social-aware motion prediction for advancing autonomous driving safety and acceptance.

This structure should help you organize your presentation effectively, covering all the essential aspects of your course and the paper abstracts.
