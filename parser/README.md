# Shopping

- [Lecture](https://cs50.harvard.edu/ai/2024/notes/6/#lecture-6)
- [Project](https://cs50.harvard.edu/ai/2024/projects/6/parser/#parser)

<br/>

### Note:
the check50 fails on correct code for this project. The test
```
np_chunk finds noun phrases that don't contain other noun phrases
```
fails with
```
Expected Output:
{'the home', 'holmes'}
```
```
Actual Output:
{'the home', 'the armchair in the home', 'holmes'}
```
while it shouldn't as discussed [here in Ed](https://edstem.org/us/courses/176/discussion/5115711)