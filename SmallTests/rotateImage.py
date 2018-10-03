def rotate_image(a):
    image_len = len(a)
    large_lst = []
    new = a
    column_counter = -1
    row_counter = 0

    for i in a:
        large_lst = large_lst + i

    for i in large_lst:
        new[row_counter][column_counter] = i
        row_counter += 1
        if row_counter == image_len:
            row_counter = 0
            column_counter -= 1


if __name__ == "__main__":
    rotate_image([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
