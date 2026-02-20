# AI Assignment 01 - Kids in the Yard

**Link to the reflection:**
 https://docs.google.com/document/d/1njP9O0FZ_oSJZa7VCYJ8dwpaCRKZ_z065ErJTa5PPJQ/edit?usp=sharing

**Answers to the Comparison Questions:**

    1. I used ChatGPT for this assignment.
    
    2. My prompt to the LLM used sections of the rubric and descriptions of the
        requirements as well as copies of all the required csv files. I basically
        showed ChatGPT the essential sections of the rubric and told it "Complete
        this assignment with a one-file python program". The inclusion of parts of
        the rubric proved necessary as this assignment had too much nuance to be
        quickly summarized in any meaningful capacity.
    
    3. The implementation of ChatGPT ended up having way less family members as
        time went on. Where my solution had exponential growth and around 900 total
        family members on average, ChatGPT's solution had single digit family
        membercounts for each generation. This is likely due to the fact that my 
        solutionallowed for children of any one individual, whereas ChatGPT opted 
        to havechildren only occur when there are 2 parents (i.e. partners). 
        Overall, Iwas shocked by how similar ChatGPT's solution was to mine. There 
        were some choices I made for implementation such as having the get_person
        function have an optional second field for last name that was None by
        default which the LLM also implemented in the same way. 
    
    4. I wouldn't change my implementation to match the LLM's. Although requiring
        two parents to produce a child is an interesting concept, it limits the
        spread of the family tree too much and produces a mostly one-dimensional
        result. If possible I'd opt to find a middle ground, since my
        implementation branched out a lot towards the end and led to MANY
        duplicates which can be complicated for a user to sift through. A change
        that I definitely would consider adapting is the inclusion of the
        various decades of duplicate names when listing them, although this
        ended up proving a bit of a challenge for the LLM that needed cleaning
        up.
    
    5. As previously stated, I would refuse to change the tree-generation
        algorithm to require two parents.
