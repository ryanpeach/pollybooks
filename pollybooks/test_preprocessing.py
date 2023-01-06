from pollybooks.preprocessing import split_text_into_n_token_strings


def test_split_text_into_n_token_strings():
    """Test this function using a small input text"""
    test_txt = """
    This is a test. This is only a test. 36

    Why is this a test? Because it's a test. 40

    You cant test this test. You can only test the test. 52
    """

    # Split the text into chunks of 15 or less tokens
    chunks = split_text_into_n_token_strings(
        test_txt, max_tokens=15, n_chars_per_token=4
    )

    assert len(chunks) == 3
