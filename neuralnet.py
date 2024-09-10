import numpy as np

#Math and Inspiration for Implementation of Neural Network:
#Omar Aflak
#https://towardsdatascience.com/math-neural-network-from-scratch-in-python-d6da9f29ce65

class Function:
    def __init__(self, func, derivative):
        self.func = func
        self.derivative = derivative

def oneHot(x, possibleValues):
    array = [0 for i in range(possibleValues)]
    array[x] = 1
    return array

def MSE(values, predicted):
    square = np.power(values - predicted, 2)
    return np.sum(square) / len(square)

def dMSE(values, predicted):
    return 2 * (predicted - values) / len(values)

def sig(x):
    return 1 / (1 + np.power(np.e, -x))

def sigPrime(x):
    return sig(x) * (1 - sig(x))

sigmoid = Function(sig, sigPrime)
meanSquaredErrorLoss = Function(MSE, dMSE)

class Layer:
    def __init__(self, nInputs, nOutputs, activation=sigmoid):
        self.weights = np.random.rand(nInputs, nOutputs) - 0.5
        self.biases = np.random.rand(1, nOutputs) - 0.5
        
        self.hiddenIn = None
        self.hiddenOut = None
        self.linearIn = None
        self.linearOut = None

        self.activation = activation

    def forward(self, input):
        self.hiddenIn = np.array(input)
        self.hiddenOut = np.dot(self.hiddenIn, self.weights) + self.biases

        self.linearIn = self.hiddenOut
        self.linearOut = self.activation.func(self.linearIn)
        return self.linearOut

    def backward(self, output, lr):
        activationError = self.activation.derivative(self.linearIn) * output

        weightsError = np.dot(self.hiddenIn.T, activationError)
        biasError = activationError
        inputError = np.dot(activationError, self.weights.T)

        self.weights -= lr * weightsError
        self.biases -= lr * biasError
        return inputError

class Network:
    def __init__(self, shape, loss=meanSquaredErrorLoss):
        self.layers = []
        for i in range(len(shape) - 1):
            self.layers.append(Layer(shape[i], shape[i + 1]))
        
        self.loss = loss
    
    def forward(self, input):
        output = input
        for layer in self.layers:
            output = layer.forward(output)
        return output
    
    def guess(self, input):
        prediction = self.forward(input)

        max = prediction[0][0]
        maxIndex = 0
        sum = 0
        for i, value in enumerate(prediction[0]):
            sum += value
            if value > max:
                max = value
                maxIndex = i
        return maxIndex, (np.round((max / sum), 2) * 100)

    def train(self, trainingData, epochs, lr, miniBatchSize):
        np.random.shuffle(trainingData)
        trainingInputs = []
        trainingLabels = []

        for sample, label in trainingData:
            trainingInputs.append(sample)
            trainingLabels.append(label)

        miniBatchIndex = np.random.randint(0, len(trainingInputs) - miniBatchSize + 1)
        for epoch in range(epochs + 1):
            e = 0
            for i, input in enumerate(trainingInputs[miniBatchIndex:miniBatchIndex + miniBatchSize]):
                output = input
                for layer in self.layers:
                    output = layer.forward(output)
                
                e += self.loss.func(trainingLabels[i], output)
                error = self.loss.derivative(trainingLabels[i], output)
                for layer in reversed(self.layers):
                    error = layer.backward(error, lr)
            
            print(f"Epoch #{epoch} Error: {e / len(trainingInputs)}")

    def save(self, filepath):
        with open(filepath, 'w') as saveFile:
            for layer in self.layers:
                weights = []
                for weight in layer.weights:
                    weights.append(list(weight))
                biases = []
                for bias in layer.biases:
                    biases.append(list(bias))
                saveFile.write(str([weights, biases]) + "\n")

    def load(self, filepath):
        with open(filepath, "r") as saveFile:
            for line, layer in zip(saveFile, self.layers):
                line.strip()
                layerData = eval(line)
                layer.weights = np.array(layerData[0])
                layer.biases = np.array(layerData[1])