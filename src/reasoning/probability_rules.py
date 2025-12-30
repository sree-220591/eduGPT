def explain_probability_bounds():
    return (
        "Probability is defined as a ratio of favorable outcomes to total possible outcomes. "
        "Since the number of favorable outcomes cannot be negative and cannot exceed the total number of outcomes, "
        "the probability of any event must lie between 0 and 1."
    )


RULES = {
    "probability between 0 and 1": explain_probability_bounds,
    "can probability be negative": explain_probability_bounds,
}
