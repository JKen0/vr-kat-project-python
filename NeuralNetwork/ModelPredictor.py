import tensorflow.keras as keras

class ModelPredictor:
    def __init__(self, model_path):
        self.model = keras.models.load_model(model_path)
    
    def predict(self, input_data): 
        # Make predictions using the loaded model
        predictions = self.model.predict(input_data)
        
        return predictions