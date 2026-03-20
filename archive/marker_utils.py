def create_start_end_markers(points):

    if not points:
        return None, None

    start = points[0]
    end = points[-1]

    return start, end