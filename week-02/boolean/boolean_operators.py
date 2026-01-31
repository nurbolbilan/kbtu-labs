age = 18
has_id = True

can_enter = (age >= 18) and has_id
print("can_enter:", can_enter)

is_weekend = False
has_free_time = True

can_play = is_weekend or has_free_time
print("can_play:", can_play)

is_raining = True
print("not is_raining:", not is_raining)

# пример посложнее
score = 78
passed = (score >= 50) and (score <= 100)
print("passed:", passed)
