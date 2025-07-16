def compute_reward(human_feedback: str, review_score: float) -> float:
    """
    Compute RL reward based on human feedback and review score.
    +1 if accepted, -1 if rejected, +0.5 if well-reviewed (score >= 0.8).
    """
    reward = 0.0
    if human_feedback == "accept":
        reward += 1.0
    elif human_feedback == "reject":
        reward -= 1.0
    if review_score >= 0.8:
        reward += 0.5
    return reward

def update_prompt_with_reward(prompt: str, reward: float, feedback: str) -> str:
    """
    Update the AI prompt based on reward and feedback for RL-based improvement.
    """
    if reward > 0:
        return prompt + f"\n\n[Note: Previous version was well received. Feedback: {feedback}]"
    elif reward < 0:
        return prompt + f"\n\n[Note: Previous version was rejected. Feedback: {feedback}]"
    else:
        return prompt 