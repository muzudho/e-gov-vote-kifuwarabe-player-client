
def do_move(position, phase, source, destination, piece, expend_time):
    src_pc = position.board[source]  # sourcePiece
    dst_pc = position.board[destination]  # destinationPiece

    # app.log.write_by_internal(f"Move> {result.group(0)} [phase]{phase:>2} [source]{source:>2} [destination]{destination} [piece]{piece} src_pc[{src_pc}] dst_pc[{dst_pc}]")
    if source != 0 and src_pc == ' * ':
        raise Exception("空マスから駒を動かそうとしました")

    # 駒を打つとき、駒台から減らす
    if source == 0:
        if phase == '+':
            src_pc = '+{}'.format(piece)
            if piece == 'FU':
                position.hands[7] -= 1
            elif piece == 'KY':
                position.hands[6] -= 1
            elif piece == 'KE':
                position.hands[5] -= 1
            elif piece == 'GI':
                position.hands[4] -= 1
            elif piece == 'KI':
                position.hands[3] -= 1
            elif piece == 'KA':
                position.hands[2] -= 1
            elif piece == 'HI':
                position.hands[1] -= 1
            else:
                raise Exception(f"+ phase={phase} piece={piece}")
        elif phase == '-':
            src_pc = '-{}'.format(piece)
            if piece == 'FU':
                position.hands[14] -= 1
            elif piece == 'KY':
                position.hands[13] -= 1
            elif piece == 'KE':
                position.hands[12] -= 1
            elif piece == 'GI':
                position.hands[11] -= 1
            elif piece == 'KI':
                position.hands[10] -= 1
            elif piece == 'KA':
                position.hands[9] -= 1
            elif piece == 'HI':
                position.hands[8] -= 1
            else:
                raise Exception(f"- phase={phase} piece={piece}")

    # 移動先に駒があれば駒台へ移動
    if phase == '+':
        if dst_pc == "-FU" or dst_pc == "-TO":
            position.hands[7] += 1
        elif dst_pc == "-KY" or dst_pc == "-NY":
            position.hands[6] += 1
        elif dst_pc == "-KE" or dst_pc == "-NK":
            position.hands[5] += 1
        elif dst_pc == "-GI" or dst_pc == "-NG":
            position.hands[4] += 1
        elif dst_pc == "-KI":
            position.hands[3] += 1
        elif dst_pc == "-KA" or dst_pc == "-UM":
            position.hands[2] += 1
        elif dst_pc == "-HI" or dst_pc == "-RY":
            position.hands[1] += 1
        elif dst_pc == "-OU":
            pass
    elif phase == '-':
        if dst_pc == "+FU" or dst_pc == "+TO":
            position.hands[14] += 1
        elif dst_pc == "+KY" or dst_pc == "+NY":
            position.hands[13] += 1
        elif dst_pc == "+KE" or dst_pc == "+NK":
            position.hands[12] += 1
        elif dst_pc == "+GI" or dst_pc == "+NG":
            position.hands[11] += 1
        elif dst_pc == "+KI":
            position.hands[10] += 1
        elif dst_pc == "+KA" or dst_pc == "+UM":
            position.hands[9] += 1
        elif dst_pc == "+HI" or dst_pc == "+RY":
            position.hands[8] += 1
        elif dst_pc == "+OU":
            pass
    else:
        raise Exception(f"Caputure piece. phase={phase}")

    # 移動元の駒を消す
    position.board[source] = " * "

    # 移動先に駒を置く
    position.board[destination] = src_pc

    # 経過時間
    if phase == '+':
        position.expend_times[1] += expend_time
    else:
        position.expend_times[2] += expend_time
