## N-gram
### 1. Defination of N-gram model
N-gram model is a predictive language model which predict next itme based on the historical context of n previous words

if we computing p(w,h), the probability of a word w and history h. for example: p(something,I want eat), the history is **I want eat** and w is **something**

#### 1.1 How to get this probability
count the number of time **I want eat** and count the number of time this followed **something**
P(w,h) = C(hw)/c(h)
