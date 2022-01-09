
import pygame

from src.characters import *
from src.tools import button
from src.bfs import bfs

class Game:
    def __init__(self) -> None:
        """
            Definições iniciais do pygame

            width, height -> representa os valores do tamanho da janela
            FPS -> representa a taxa de quadro do jogo
            game_over -> representa o estado atual do jogo, utilizado para manter o loop principal
            position -> representa os locais disponiveis nos dois lados e na jangada
            right_side -> armazena os objetos, canibais ou missionarios, que estão no lado direito do rio
            left_side -> armazena os objetos, que estaõ no lado esquerdo do rio
            current_raft -> armazena os objetos que estão atualmente utiizando a jangada
            raft -> representa o objeto jangada
        """
        pygame.init()
        pygame.display.set_caption('Cannibal and Missionaries')

        # display settings
        self.width, self.height = 1100 , 688
        self.FPS = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.game_over = False

        self.background = pygame.image.load('static/images/background.png')

        self.positon = {}

        self.right_side = {}
        self.left_side = {}

        self.current_raft = []

        self.raft = Character(self.screen, (600, 420), 'raft')

    def check_events(self):
        """ Função que verifica eventos do teclado """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
                exit()

    def reset(self):
        """
            Função responsavel por inicializar as posições iniciais de todos os elementos da tela
        """
        self.position = {'right': [(930, 210), (860, 290), (940, 310), (980, 400), (860, 470), (960, 500)],
                         'left': [(210, 210), (150, 280), (20, 340), (310, 220), (80, 250), (5, 450)],
                         'raft': [(620, 330), (700, 320)]}

        self.right_side = {'cannibal': [Character(self.screen, self.choice_position_land('l'), 'cannibal'), 
                                       Character(self.screen, self.choice_position_land('l'), 'cannibal'), 
                                       Character(self.screen, self.choice_position_land('l'), 'cannibal')],
                           'missionary': [Character(self.screen, self.choice_position_land('l'), 'missionary'), 
                                           Character(self.screen, self.choice_position_land('l'), 'missionary'), 
                                           Character(self.screen, self.choice_position_land('l'), 'missionary')]}
        self.left_side = {'cannibal': [],
                          'missionary': []}

    def render_cannibal_missionary(self):
        """
            Renderiza canibais e missionarios nos dois lados do rio
        """
        for i in self.right_side.values():
            for j in i:
                j.render()
        
        for i in self.left_side.values():
            for j in i:
                j.render()

    def render_everything(self):
        """
            Renderiza o fundo e a jangada
        """
        self.screen.blit(self.background, (0, 0))

        self.raft.render()
    
    def choice_position_land(self, side):
        """
            responsavel por escolher uma posição disponivel em um dos lado do rio
            retorna uma posição disponivel na "terra" para um objeto
        """
        if side == 'r':
            position = self.position['left'].pop(0)
            return position
        elif side == 'l':
            position = self.position['right'].pop(0)
            return position


class GameMain(Game):
    def __init__(self) -> None:
        super().__init__()

    def run_game(self):

        self.reset()

        # iniciamos a função que vai procurar o melhor caminho possivel dando a origem e o destino
        states = bfs('00r33', '33l00')

        self.game(states)

        while not self.game_over:

            # Verifica eventos do teclado
            self.check_events()

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))

            self.render_cannibal_missionary()
            self.raft.render()

            if button(20, 'Play again?', 274, 100, 250, 50, True, 'play', self.screen):
                game = GameMain()
                game.run_game()

            button(20, 'Exit??', 578, 100, 250, 50, True, 'exit', self.screen)

            pygame.display.update()

    def choice_position_raft(self):
        """
            Responsavel por retornar uma posição disponivel na jangada
        """
        position = self.position['raft'].pop(0)

        return position
    
    def game(self, states):
        """
            Realiza a animação
        """
        self.render_everything()
        self.render_cannibal_missionary()

        pygame.display.update()
        pygame.time.wait(250)

        # realizamos um for para cada passo necessario
        for s in range(len(states) - 1):

            # guarda o lado que a jangada esta
            side = states[s][2]

            # calcula a quantidade de canibais e missionarios que vão ser 
            # transportados para o outro lado, exemplor: (1, 0) = 1 canibal, 0 missionario
            step = (abs(int(states[s][3]) - int(states[s + 1][3])), abs(int(states[s][4]) - int(states[s + 1][4])))

            # verficamos o lado que a jangada esta e então verificamos a quantidade de canibais e missionarios
            if side == 'r':
                for i in range(step[0]):
                    cannibal = self.right_side['cannibal'][0]

                    self.position['right'].append(cannibal.position)

                    cannibal.change_position(self.choice_position_raft())

                    self.right_side['cannibal'].remove(cannibal)

                    self.current_raft.append(cannibal)

                for i in range(step[1]):
                    missionary = self.right_side['missionary'][0]

                    self.position['right'].append(missionary.position)

                    missionary.change_position(self.choice_position_raft())

                    self.right_side['missionary'].remove(missionary)

                    self.current_raft.append(missionary)

            elif side == 'l':
                for i in range(step[0]):
                    cannibal = self.left_side['cannibal'][0]

                    self.position['left'].append(cannibal.position)

                    cannibal.change_position(self.choice_position_raft())

                    self.left_side['cannibal'].remove(cannibal)

                    self.current_raft.append(cannibal)

                for i in range(step[1]):
                    missionary = self.left_side['missionary'][0]

                    self.position['left'].append(missionary.position)

                    missionary.change_position(self.choice_position_raft())

                    self.left_side['missionary'].remove(missionary)

                    self.current_raft.append(missionary)
                        
            self.move(side)

            pygame.time.wait(100)

            self.next_move(side)

            self.render_everything()
            self.render_cannibal_missionary()
            pygame.display.update()

            pygame.time.wait(250)

    def move(self, side):
        """
            Resposavel por realizar a animação da jangada com os e os elementos que estão na jangada
        """
        if side == 'l':

            while self.raft.position < (600, 420):
                self.raft.position = self.raft.position[0] + 10, self.raft.position[1]

                self.render_everything()
                self.render_cannibal_missionary()

                for character in self.current_raft:
                    character.position = character.position[0] + 10, character.position[1]
                    character.render()


                pygame.display.update()

                self.FPS.tick(20)

        elif side == 'r':

            while self.raft.position > (260, 420):
                self.raft.position = self.raft.position[0] - 10, self.raft.position[1]

                self.render_everything()
                self.render_cannibal_missionary()

                for character in self.current_raft:
                    character.position = character.position[0] - 10, character.position[1]
                    character.render()


                pygame.display.update()

                self.FPS.tick(20)
        
        pygame.time.wait(250)

    def next_move(self, side):
        """
            Responsavel por realizar retirada dos elementos que estavam na jangada e 
            agora precisam ir para terra quando a animação de atravessar o rio acaba
        """

        if side == 'r':
            for character in self.current_raft:
                character.change_position(self.choice_position_land(side))

                if character.type() == 'cannibal':
                    self.left_side['cannibal'].append(character)
                else:
                    self.left_side['missionary'].append(character)

            self.position['raft'] = [(280, 330), (360, 320)]

        else:
            for character in self.current_raft:
                character.change_position(self.choice_position_land(side))

                if character.type() == 'cannibal':
                    self.right_side['cannibal'].append(character)
                else:
                    self.right_side['missionary'].append(character)
            
            self.position['raft'] = [(620, 330), (700, 320)]

        self.current_raft.clear()


class GameLoad(Game):
    def __init__(self) -> None:
        super().__init__()

    def run_game(self):
        self.reset()
        while not self.game_over:

            # Verifica eventos do teclado
            self.check_events()

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))

            if button(20, 'Play?', 274, 100, 250, 50, True, 'play', self.screen):
                game = GameMain()
                game.run_game()

            button(20, 'Exit??', 578, 100, 250, 50, True, 'exit', self.screen)

            self.render_cannibal_missionary()
            self.raft.render()

            pygame.display.update()


if __name__ == '__main__':
    game = GameLoad()
    game.run_game()
