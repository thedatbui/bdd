class Quest:
    def __init__(self, id, name, description, difficulty, reward):
        """
        Initialize a Quest object.

        Args:
            id (int): Unique identifier for the quest
            name (str): Name of the quest
            description (str): Description of the quest
            difficulty (str): Difficulty level of the quest
            reward (int): Reward for completing the quest
        """
        self.id = id
        self.name = name
        self.description = description
        self.difficulty = difficulty
        self.reward = reward

    def __str__(self):
        return f"Quest(name={self.name}, description={self.description}, difficulty={self.difficulty}  ,reward={self.reward})"

    def __repr__(self):
        return self.__str__()

    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_description(self):
        return self.description
    
    def get_difficulty(self):
        return self.difficulty
    
    def get_reward(self):
        return self.reward
    
    def set_id(self, id):
        self.id = id

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    def set_reward(self, reward):
        self.reward = reward