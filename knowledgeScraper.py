from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Set up WebDriver
# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service)
driver = webdriver.Chrome()

# Path to save the file in the Documents folder
save_path = 'scraperesults.txt'


# Function to scrape questions and answers from a quiz
def scrape_quiz(url):
    driver.get(url)
    quiz_data = []

    # Loop through a reasonable number of expected questions
    for i in range(1, 30):
        try:
            # Find the heading
            heading_element = driver.find_element(By.ID, f'question{i}')

            # Get the heading text
            heading_text = heading_element.find_element(By.XPATH, './/div[@class="text-left"]/preceding-sibling::h2').text.strip()
            print(f"Heading {i}: {heading_text}")

            # Get the question text
            question_text = heading_element.find_element(By.XPATH, './/div[@class="text-left"]').text.strip()
            print(f"Question {i}: {question_text}")

            # Initialize correct_answers list
            correct_answers = []

            # Find all answer elements (checkboxes)
            answer_elements = heading_element.find_elements(By.XPATH, './/div[@class="form-check"]')
            for answer in answer_elements:
                checkbox = answer.find_element(By.TAG_NAME, 'input')
                if checkbox.get_attribute('data-ans') == '1':  # Check for correct answers
                    label = answer.find_element(By.TAG_NAME, 'label')
                    correct_answers.append(label.text.strip())
                    print(f"Correct answer found: {label.text.strip()}")

            # Find all answer elements (dropdown)
            dropdown_elements = heading_element.find_elements(By.XPATH, ".//select[@class='form-control']")
            for dropdown in dropdown_elements:
                correct_answer_index = dropdown.get_attribute('data-ans')  # Get the correct answer index
                # Find the corresponding label for the dropdown
                dropdown_label = dropdown.find_element(By.XPATH, './preceding-sibling::label/p').text.strip()
                # Find the corresponding answer text from the answer list
                answer_list = heading_element.find_elements(By.XPATH, ".//ol[@class='padded-ol text-left']/li")
                if 0 <= int(correct_answer_index) < len(answer_list):
                    correct_answer_text = answer_list[int(correct_answer_index)].text.strip()  # Get the answer text
                    correct_answers.append(f"{dropdown_label}: {correct_answer_text}")
                    print(f"Correct answer found for '{dropdown_label}': {correct_answer_text}")

            # Find all answer elements (short answer)
            short_answer_inputs = heading_element.find_elements(By.XPATH, './/input[@type="text"]')
            for input_element in short_answer_inputs:
                hidden_value = heading_element.find_element(By.XPATH, f'//input[@id="sa{i}"]').get_attribute('value')
                if hidden_value:
                    correct_answers.append(hidden_value)
                    print(f"Short answer found: {hidden_value}")

            # Join correct answers together and handle no answers found
            correct_answer = ("\nA: ").join(correct_answers) if correct_answers else "No correct answer found"

            # Store the question and correct answer in quiz_data
            quiz_data.append((f"Heading: {heading_text}", f"Q: {question_text}", f"A: {correct_answer}"))

            # Store path of the next arrow button
            button_path = "//div[contains(@id, 'question') and not(contains(@class, 'd-none'))]//button[contains(@class, 'btn-forward')]"

            # Find button and click it
            next_button = driver.find_element(By.XPATH, button_path)
            next_button.click()

        except:
            print(f"Could not find anymore questions.\n")
            break  # Exit the loop if no more questions are found

    return quiz_data

# List of quiz URLs
quiz_urls = [
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=1&s=1",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=1&s=2",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=1&s=3",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=1&s=4",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=1&s=5",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=1&s=6",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=1&s=7",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=1&s=8",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=2&s=1",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=2&s=2",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=2&s=3",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=2&s=4",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=2&s=6",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=2&s=7",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=3&s=1",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=3&s=2",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=3&s=3",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=3&s=4",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=3&s=5",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=3&s=6",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=3&s=7",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=3&s=8",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=4&s=1",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=4&s=2",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=4&s=3",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=4&s=4",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=4&s=5",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=5&s=1",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=5&s=2",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=5&s=3",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=5&s=4",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=5&s=5",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=5&s=6",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=6&s=1",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=6&s=2",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=6&s=3",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=6&s=4",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=7&s=1",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=7&s=2",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=7&s=3",
    "https://gaia.cs.umass.edu/kurose_ross/knowledgechecks/problem.php?c=7&s=4"
    # Add more quiz URLs here...
]

# List to store data for all quizzes
all_quiz_data = []

# Scrape each quiz and add the data to all_quiz_data
for url in quiz_urls:
    chapter_number = url.split('c=')[1].split('&')[0]  # Extract chapter number from URL
    section_number = url.split('s=')[1].split('&')[0]  # Extract section number from URL
    print(f"Scraping quiz at {url}")
    quiz_data = scrape_quiz(url)
    all_quiz_data.append((chapter_number, section_number, quiz_data))  # Store chapter and section number with quiz data
# After all quizzes scraped, save the data to a file
with open(save_path, "w") as file:
    file.write("Computer Networking Knowledge Checks Questions and Answers\n\n\n")
    for chapter_number, section_number, quiz in all_quiz_data:
        file.write(f"Chapter {chapter_number}, Section {section_number}\n\n")  # Print chapter and section number
        for quiz_index, (question, description, answer) in enumerate(quiz, start=1):
            file.write(f"Quiz {quiz_index}:\n")
            file.write(f"{question}\n{description}\n{answer}\n\n")
        file.write("\n")


# Close the browser
driver.quit()

print(f"Scraping complete. Data saved to {save_path}")
