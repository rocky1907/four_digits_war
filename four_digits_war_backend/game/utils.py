def count_picas_fijas(secret, guess):
    fijas = sum(s == g for s, g in zip(secret, guess))
    picas = sum(min(secret.count(d), guess.count(d)) for d in set(guess)) - fijas
    return picas, fijas
