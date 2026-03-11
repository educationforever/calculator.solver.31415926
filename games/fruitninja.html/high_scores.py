"""
High score management for the game
"""
import json
import os
import time
from datetime import datetime

class HighScoreManager:
    """Manages high scores for the game"""
    
    def __init__(self, scores_file="fruit_ninja_scores.json"):
        self.scores_file = scores_file
        self.high_scores = self.load_scores()
        
    def load_scores(self):
        """Load high scores from file"""
        try:
            if os.path.exists(self.scores_file):
                with open(self.scores_file, 'r') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            print(f"Error loading high scores: {e}")
            return []
            
    def save_scores(self):
        """Save high scores to file"""
        try:
            with open(self.scores_file, 'w') as f:
                json.dump(self.high_scores, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving high scores: {e}")
            return False
            
    def add_score(self, score, player_name="Player"):
        """Add a new high score"""
        new_entry = {
            "name": player_name,
            "score": score,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Add to list and sort
        self.high_scores.append(new_entry)
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)
        
        # Keep only top 10 scores
        if len(self.high_scores) > 10:
            self.high_scores = self.high_scores[:10]
            
        # Save to file
        self.save_scores()
        
        # Return position in high scores (1-based)
        return self.get_score_position(score)
        
    def get_score_position(self, score):
        """Get position of a score in the high scores list (1-based)"""
        for i, entry in enumerate(self.high_scores):
            if score >= entry["score"]:
                return i + 1
        return len(self.high_scores) + 1 if len(self.high_scores) < 10 else 0
        
    def is_high_score(self, score):
        """Check if a score qualifies as a high score"""
        if len(self.high_scores) < 10:
            return True
        return score > self.high_scores[-1]["score"]
        
    def get_high_scores(self):
        """Get the list of high scores"""
        return self.high_scores
