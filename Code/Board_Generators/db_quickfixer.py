from DatabaseMaker import get_database_data, save_updated_database 

if __name__ == '__main__':
    db = get_database_data()

    for board_size in db:
        b_size = db.get(board_size)
        for board_num in b_size:
            # fix board
            for row in b_size.get(board_num).get("board"):
                for idx, val in enumerate(row):
                    row[idx] = int(val)
            # fix coordinates
            for coord_set in b_size.get(board_num).get("coordinates"): 
                coord_set[2] = int(coord_set[2])
    
    save_updated_database(db)