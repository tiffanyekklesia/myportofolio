Name    : Tiffany

NPM     : 2506546062

Class   : PBP E

### Assignmnet 1
1. In Tutorial 1 and Individual Assignment 1, you were given the freedom to decide your portfolio website’s design. When you designed the HTML structure you used, did you use semantic HTML5 elements such as <section>, <article>, or <aside>? If so, how did those elements help you build the static web? If not, why did your design’s needs stay met without them?
Answer  : I used semantic HTML5 elements in my portofolio. I used <section> to separate major parts of the page, such as the About Me, Projects, and Skills sections. Within the projects and Skills sections, I used <article> to represent individual pieces of content. This made the HTML structure easier to understand and maintain because the structure of the page reflects the meaning of its content rather than only its visual appearance. I also used <nav> for the navigation links and <footer> for the information at the bottom of the page.

2. When you set up your CSS to stay responsive, what layout challenges did you encounter? How did you evaluate which elements needed to be repositioned or prioritized in size when moving from the desktop view to mobile?
Answer  : One of the main challenges was maintaining the two-column layout of the About Me section while keeping the profile photo and text readable on smaller screens. I used CSS Grid for the desktop layout and changed it into a single column layout through media queries on smaller screens. I also changed the Projects grid from three columns into one column on smaller screens. I prioritized the profile information,photo, and navigation because they are the most important elements of the page. I evaluated the layoyt by testing teh website at different browser widths and checking whether text became crowded, elements overflowed, or buttons and navigation links becmae difficult to use.

3. The website you’ve built right now is a purely static web. What limitations did you feel while trying to present your portfolio’s information optimally? Based on those limitations, what dynamic functionality would you most want to prepare and add in the next iteration of the project?
Answer  : The main limitation of a static website is that the content has to be edited directly on the HTML files. For example, adding a new project or updating infomration requires manually changing the source code. A dynamic version could store projects and personal information in a database so that the content could be managed without directly editing the HTML. In thenext iteration, I would like to add dynamic project section where projects can be stored, updated, an ddisplayed using Django's MVT architecture.

### Assignment 2
1. How does the flow of an HTTP request to your Django website work, starting from the URL that the user accesses until the HTML response is displayed? Explain how MVT is applied in this flow.
Answer  : When a user accesses a URL such as /projects/, Django first matches the URL with the URL patterns defined in main/urls.py. The URL is connected to the show_projects view in main/views.py. The view retrieves Project objects from the database through the Project model. The retrieved data is then placed into a context dictionary and passed to the project.html template. Django's template system uses the context data to generate the final HTML, which is then returned as the HTTP response and displayed in the user's browser. In this flow, the Model handles the database data, the View handles the request and application logic, and the Template handles how the data is presented.

2. Why is it better to use a model to store portfolio data compared to hardcoding the data in an HTML template?
Answer  : Using a model is better because portfolio data can be stored and managed separately from the HTML presentation. In my project, the Project model stores information such as the project name, description, technologies, and project URL in the database. The template then retrieves and displays this data dynamically using Django Template Language. This makes the website easier to update because adding or changing a project does not require manually editing the HTML structure. It also makes the portfolio more scalable because more project objects can be added to the database and displayed automatically.

3. What is the difference between makemigrations and migrate in Django?
Answer  : makemigrations is used to detect changes in Django models and create migration files that describe those changes. For example, after adding the Project model, I ran python manage.py makemigrations and Django created the 0002_project.py migration file. On the other hand, migrate applies the migration files to the database, so the changes defined by the migrations actually take effect in the database. In my project, I ran python manage.py migrate after makemigrations to create the database structure for the Project model.

### AI disclosure
I used ChatGPT as an AI-assisted learning and development tool during this assigment.
AI assistance was used to:
- explain HTML5 and CSS3 concepts used in the implementations
- help plan the HTML structure and semantic elements
- suggest CSS layouts and responsive design approaches
My main prompting approach was to ask the AI to explain the reasoning behind the suggested HTML and CSS rather than only requesting a finished solution. AI-generated suggestions were not accepted blindly. I manually checked the resulting structure, corrected personal information, adjusted the layout, and tested the implemenattion in the browser.