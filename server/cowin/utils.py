def age_filter(available_centers, age=None):
    if age is None:
        return available_centers

    filtered = []
    for center in available_centers:
        f_sessions = []

        for session in center["sessions"]:
            if session["min_age_limit"] == int(age):
                f_sessions.append(session)
        if len(f_sessions):
            center["sessions"] = f_sessions
            filtered.append(center)

    return filtered
