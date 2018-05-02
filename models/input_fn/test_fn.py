import pickle
event_vectors = pickle.load(open("event_vectors.p", "rb"))
print(len(event_vectors[0]))