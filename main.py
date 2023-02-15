def nameHelper(s1:str,s2:str) -> int:
    """
        This function is the helper function for the isSimilarFunction. It checks the total number of edits required for the two strings to be similar.
        For example:
            "sjislLxiXZmXLXrA","sjislLxiXZmXLXr"
            As, the maximum number of edits required are 1
            This is at he last index, where the "A" can be deleted in the first string
        
        So, the algorithm goes like, finding out the minimum number of edits required on first string to make it equal to the second one.

        There will be two cases to be considered here:
        1. Case 1: when, s1[i]=s2[i]
        In this case, we skip the ith position and make the number of edits of whole problem equal to the edits of s1[i+1:n] and s2[i+1:n]

        2. when, s1[i]!=s2[i]
        Here, we'll be finding the edits required on the bases of insert, delete, substitute
            * Insert s2[i] in s1: here our number of edits will be equal to 1 + s1[i:n] and s2[i+1:m], as we have already made the ith character of s2 equal to s1 by adding it to s1

            * Delete s1[i]: here our number of edits will be equal to 1 + s1[i+1:n] and s2[i:m], as we have deleted the ith character from s1

            * substitute s1[i] with s2[i]: here out number of edits will be 1 + s1[i+1:n] and s2[i+1:m]
        
        The overall number of edits will be the minimum of all three operations.

        Args:
        - s1 (str): The first string to be compared.
        - s2 (str): The second string to be compared.
        
        Returns:
        int: minimum nuumber of edits to be performed inorder to make the two string equal
        
        Examples:
        >>> nameHelper("kitten", "sitting")
        3
        >>> nameHelper("flaw", "lawn")
        2
    """

    n = len(s1)
    m = len(s2)

    minPrevRow = None
    minCurrRow = list(range(1, m+1)) + [0]

    for i in range(n):
        minPrevRow, minCurrRow = minCurrRow, [0]*m+[i+1]
        for j in range(m):
            deleteCost = minPrevRow[j] + 1
            additionCost = minCurrRow[j-1]+1
            substitutionCost = minPrevRow[j-1] + (s1[i]!=s2[j])
            minCurrRow[j] = min(deleteCost, additionCost, substitutionCost)
    
    return minCurrRow[m-1]



def isSimilarName(s1:str, s2:str) -> bool:
    """
        This function checks whether the two string names are similar of not.
        For example:
            "sjislLxiXZmXLXrA" ~ "sjislLxiXZmXLXr"
            As, the maximum number of edits required are 1
            This is at he last index, where the "A" can be deleted in the first string

            Since 1<5, the two strings are considered as to be similar
        
        Args:
        - s1 (str): first location name
        - s2 (str): second location name

        Returns:
        bool: are the two name similar or not

        Examples:
            >>> isSimilarName("kitten", "sitting")
            True
            >>> isSimilarName("flaw", "lawn")
            True
    """

    return nameHelper(s1,s2)<5


def isCloseProximity(loc1:tuple[int, int], loc2:tuple[int,int]) -> bool:
    """
        This function checks whether the two positions on the globe are close enough to each other or not.
        For example:
            (41.49008, -71.312796) !~ (41.49008, -71.312796)
            The distance between these two points is 866455.4329098684 meters

            Since 866455< > 200, the two locations are considered as to be not similar
        
        This function uses the great circle distance.
        d = r * cos^-1[cos a cos b cos(x-y) + sin a sin b]

        Args:
        - loc1:tuple[int, int]: first location on the globe; (lat,long)
        - loc2:tuple[int, int]: second location on the globe; (lat,long)

        Returns:
        bool: are the two location close enough or not, is the distance between them less than or equal to 200 meters

        Examples:
            >>> isCloseProximity((41.49008, -71.312796), (41.49008, -71.312796))
            False
            >>> isCloseProximity((41.49008, -71.312796), (41.49008, -74.312796))
            False
    """

    from geopy.distance import great_circle

    distance = great_circle(loc1, loc2).meters

    return distance <= 200

def main():
    """
        The main driver function that iterates over the pairs in the dataframe to check for the similarity in the dataframe based on the given conditions.

        The above code performs data processing on a CSV file to identify similar rows based on proximity and name similarity. The code performs the following steps:

        1. Imports the required libraries (pandas and tqdm)
        2. Reads a CSV file "assignment_data.csv" into a pandas dataframe
        3. Adds a new column 'is_similar' with default value 0 to the dataframe
        4. Converts the dataframe into a dictionary object and saves it to a variable 'data'
        5. Creates a list of dictionaries 'res' from the 'data' dictionary object
        6. Uses the 'combinations' function from the 'itertools' library to generate all possible pairs of rows from the 'data' list
        7. Iterates over each pair of rows and calls two functions 'isCloseProximity' and 'isSimilarName' to determine the proximity and name similarity between the two rows
        8. If the proximity and name similarity between the two rows are determined to be similar, then the 'is_similar' value for both rows is updated to 1
        9. Converts the 'res' list of dictionaries back into a pandas dataframe and saves it to the variable 'df'
        10. Writes the 'df' dataframe to a new CSV file 'result.csv'
        11. Clears the 'res', 'data', and 'df' variables from memory

    """

    import pandas as pd
    from tqdm import tqdm
    data = pd.read_csv("assignment_data.csv")

    data['is_similar'] = 0

    data = data.to_dict("index")

    from itertools import combinations

    allPairs = list(combinations(data, 2))

    for pair in tqdm(allPairs):
        idxOne = pair[0]
        idxTwo = pair[1]
        rowOne = data[idxOne]
        rowTwo = data[idxTwo]
        distanceSimilar = isCloseProximity((rowOne['latitude'], rowOne['longitude']), (rowTwo['latitude'], rowTwo['longitude']))

        if not distanceSimilar:
            continue

        nameSimilar = isSimilarName(rowOne['name'], rowTwo['name'])

        if nameSimilar:
            rowOne["is_similar"]=1
            rowTwo["is_similar"]=1
            data[idxOne] = rowOne
            data[idxTwo] = rowTwo

    df = pd.DataFrame(data).T

    df.to_csv("output.csv", index=False)

    del data
    del df

if __name__=="__main__":
    import time

    start_time = time.time()

    main()

    end_time = time.time()

    print("Time taken: {:.6f} seconds".format(end_time - start_time))



# Execution time -> 497.68 seconds