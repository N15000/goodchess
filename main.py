from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

# Chess piece class
class Piece:
    def __init__(self, type, color, position):
        self.type = type
        self.color = color
        self.position = position
        self.hasMoved = False

# Initialize board
def initializeBoard():
    board = [[None for _ in range(8)] for _ in range(8)]
    back_rank = ['Rook','Knight','Bishop','Queen','King','Bishop','Knight','Rook']
    for col, p in enumerate(back_rank):
        board[0][col] = Piece(p, 'White', (0,col))
        board[1][col] = Piece('Pawn', 'White', (1,col))
        board[7][col] = Piece(p, 'Black', (7,col))
        board[6][col] = Piece('Pawn', 'Black', (6,col))
    return board

# Get valid moves
def getValidMoves(board, piece):
    r, c = piece.position
    moves = []
    def in_bounds(r,c): return 0<=r<8 and 0<=c<8

    if piece.type == 'Pawn':
        step = 1 if piece.color=='White' else -1
        if in_bounds(r+step,c) and board[r+step][c] is None:
            moves.append((r+step,c))
        for dc in [-1,1]:
            if in_bounds(r+step,c+dc) and board[r+step][c+dc] is not None:
                if board[r+step][c+dc].color != piece.color:
                    moves.append((r+step,c+dc))

    elif piece.type == 'Rook':
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            while in_bounds(nr,nc):
                if board[nr][nc] is None:
                    moves.append((nr,nc))
                elif board[nr][nc].color != piece.color:
                    moves.append((nr,nc))
                    break
                else:
                    break
                nr += dr
                nc += dc

    elif piece.type == 'Knight':
        for dr,dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
            nr, nc = r+dr, c+dc
            if in_bounds(nr,nc) and (board[nr][nc] is None or board[nr][nc].color != piece.color):
                moves.append((nr,nc))

    elif piece.type == 'Bishop':
        for dr, dc in [(-1,-1),(-1,1),(1,-1),(1,1)]:
            nr, nc = r+dr, c+dc
            while in_bounds(nr,nc):
                if board[nr][nc] is None:
                    moves.append((nr,nc))
                elif board[nr][nc].color != piece.color:
                    moves.append((nr,nc))
                    break
                else: break
                nr += dr; nc += dc

    elif piece.type == 'Queen':
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            nr, nc = r+dr, c+dc
            while in_bounds(nr,nc):
                if board[nr][nc] is None:
                    moves.append((nr,nc))
                elif board[nr][nc].color != piece.color:
                    moves.append((nr,nc))
                    break
                else: break
                nr += dr; nc += dc

    elif piece.type == 'King':
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr==0 and dc==0: continue
                nr, nc = r+dr, c+dc
                if in_bounds(nr,nc) and (board[nr][nc] is None or board[nr][nc].color != piece.color):
                    moves.append((nr,nc))

    return moves

# Main App
class ChessApp(App):
    def build(self):
        self.TURN = 'White'
        self.selected = None
        self.valid_moves = []
        self.board = initializeBoard()

        self.layout = FloatLayout()
        self.buttons = [[None for _ in range(8)] for _ in range(8)]

        # Create 8x8 board using FloatLayout
        for r in range(8):
            for c in range(8):
                b = Button(
                    size_hint=(1/8, 1/8),
                    pos_hint={'x': c/8, 'y': 1 - (r+1)/8}
                )
                color = (0.94,0.85,0.71,1) if (r+c)%2==0 else (0.71,0.53,0.38,1)
                b.background_color = color
                b.bind(on_release=lambda btn, row=r, col=c: self.on_click(row,col))
                self.layout.add_widget(b)
                self.buttons[r][c] = b

        self.update_board()
        return self.layout

    def update_board(self):
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                btn = self.buttons[r][c]
                if piece is None:
                    btn.text = ''
                else:
                    btn.text = piece.type[0]
                    btn.color = (0,0,0,1) if piece.color=='White' else (1,0,0,1)

                if (r,c) in self.valid_moves:
                    btn.background_color = (0,1,0,0.6)
                else:
                    btn.background_color = (0.94,0.85,0.71,1) if (r+c)%2==0 else (0.71,0.53,0.38,1)

    def on_click(self,row,col):
        clicked_piece = self.board[row][col]
        if self.selected is None:
            if clicked_piece is not None and clicked_piece.color == self.TURN:
                self.selected = clicked_piece
                self.valid_moves = getValidMoves(self.board,self.selected)
        else:
            if (row,col) in self.valid_moves:
                self.board[row][col] = self.selected
                r,c = self.selected.position
                self.board[r][c] = None
                self.selected.position = (row,col)
                self.selected.hasMoved = True
                self.TURN = 'Black' if self.TURN=='White' else 'White'
            self.selected = None
            self.valid_moves = []

        self.update_board()

if __name__ == '__main__':
    ChessApp().run()