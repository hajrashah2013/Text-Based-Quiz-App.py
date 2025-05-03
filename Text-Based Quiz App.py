import pygame
import sys
import json

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quiz App")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Fonts
title_font = pygame.font.SysFont('Arial', 40, bold=True)
question_font = pygame.font.SysFont('Arial', 28)
option_font = pygame.font.SysFont('Arial', 24)
button_font = pygame.font.SysFont('Arial', 22, bold=True)
feedback_font = pygame.font.SysFont('Arial', 26)

# Quiz data (can be loaded from a JSON file)
quiz_data = [
    {
        "question": "What is the capital of France?",
        "options": ["London", "Paris", "Berlin", "Madrid"],
        "answer": 1
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "answer": 1
    },
    {
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "answer": 1
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"],
        "answer": 2
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
        "answer": 3
    }
]

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        
        text_surf = button_font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class QuizApp:
    def __init__(self):
        self.questions = quiz_data
        self.current_question = 0
        self.score = 0
        self.selected_option = None
        self.feedback = ""
        self.feedback_color = BLACK
        self.quiz_complete = False
        
        # Create option buttons
        self.option_buttons = []
        for i in range(4):
            btn = Button(150, 250 + i*70, 500, 60, "", LIGHT_BLUE, GRAY)
            self.option_buttons.append(btn)
            
        # Create navigation buttons
        self.next_btn = Button(550, 500, 150, 50, "Next", LIGHT_BLUE, GRAY)
        self.quit_btn = Button(100, 500, 150, 50, "Quit", LIGHT_BLUE, GRAY)
        
    def load_question(self):
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            
            # Update option buttons with current question options
            for i, option in enumerate(question["options"]):
                self.option_buttons[i].text = option
                
            self.selected_option = None
            self.feedback = ""
        else:
            self.quiz_complete = True
            
    def check_answer(self):
        if self.selected_option is not None:
            correct_answer = self.questions[self.current_question]["answer"]
            if self.selected_option == correct_answer:
                self.score += 1
                self.feedback = "Correct!"
                self.feedback_color = GREEN
            else:
                correct_text = self.questions[self.current_question]["options"][correct_answer]
                self.feedback = f"Incorrect! The correct answer was: {correct_text}"
                self.feedback_color = RED
                
    def draw(self):
        screen.fill(WHITE)
        
        # Draw title
        title = title_font.render("Quiz Game", True, BLUE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        # Draw score
        score_text = button_font.render(f"Score: {self.score}/{len(self.questions)}", True, BLACK)
        screen.blit(score_text, (WIDTH - 150, 30))
        
        if not self.quiz_complete:
            # Draw question
            question = self.questions[self.current_question]["question"]
            question_surf = question_font.render(question, True, BLACK)
            screen.blit(question_surf, (50, 150))
            
            # Draw options
            for i, button in enumerate(self.option_buttons):
                button.draw(screen)
                
                # Highlight selected option
                if i == self.selected_option:
                    pygame.draw.rect(screen, GREEN, button.rect, 3, border_radius=10)
                    
            # Draw feedback
            if self.feedback:
                feedback_surf = feedback_font.render(self.feedback, True, self.feedback_color)
                screen.blit(feedback_surf, (50, 450))
                
            # Draw navigation buttons
            self.next_btn.draw(screen)
            self.quit_btn.draw(screen)
            
            # Update next button text if it's the last question
            if self.current_question == len(self.questions) - 1:
                self.next_btn.text = "Finish"
            else:
                self.next_btn.text = "Next"
        else:
            # Quiz complete screen
            completion_text = title_font.render("Quiz Complete!", True, BLUE)
            screen.blit(completion_text, (WIDTH//2 - completion_text.get_width()//2, 150))
            
            score_text = question_font.render(f"Your final score: {self.score}/{len(self.questions)}", True, BLACK)
            screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 250))
            
            percentage = (self.score / len(self.questions)) * 100
            performance_text = question_font.render(
                f"Performance: {percentage:.0f}%", 
                True, 
                GREEN if percentage >= 70 else RED
            )
            screen.blit(performance_text, (WIDTH//2 - performance_text.get_width()//2, 300))
            
            self.quit_btn.draw(screen)
            
    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # Check option button clicks
            if not self.quiz_complete and not self.feedback:
                for i, button in enumerate(self.option_buttons):
                    if button.is_clicked(mouse_pos, event):
                        self.selected_option = i
                        
            # Check navigation button clicks
            if self.next_btn.is_clicked(mouse_pos, event):
                if self.quiz_complete:
                    pygame.quit()
                    sys.exit()
                elif self.feedback:
                    self.current_question += 1
                    if self.current_question < len(self.questions):
                        self.load_question()
                    else:
                        self.quiz_complete = True
                elif self.selected_option is not None:
                    self.check_answer()
                    
            if self.quit_btn.is_clicked(mouse_pos, event):
                pygame.quit()
                sys.exit()
                
        # Update button hover states
        if not self.quiz_complete:
            for button in self.option_buttons:
                button.check_hover(mouse_pos)
                
        self.next_btn.check_hover(mouse_pos)
        self.quit_btn.check_hover(mouse_pos)

def main():
    clock = pygame.time.Clock()
    quiz = QuizApp()
    quiz.load_question()
    
    while True:
        quiz.handle_events()
        quiz.draw()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()