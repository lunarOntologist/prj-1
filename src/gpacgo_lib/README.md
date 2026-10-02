Computes the credit-weighted GPA from a list of dictionary-like enrollments.
    Each enrollment is expected to provide a 'grade' key (e.g. 'A+', 'B-', ...)
    and a 'credits' key (the number of credit hours for the course).
    Enrollments with no grade yet, or an unrecognized grade, are ignored.
    Returns 0 when there are no graded credits to average.

GitHub URL: https://github.com/lunarOntologist/prj-1