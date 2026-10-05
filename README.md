Name    : Tiffany

NPM     : 2506546062

Class   : PBP E

### Assignment 1
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

### Assignment 3
1 Explain why we use Django’s `ModelForm` instead of creating HTML forms manually. Additionally, explain why we are required to add `{% csrf_token %}` to these forms?
Answer  : Django's `ModelForm` makes it easier to create forms because the form fields can be generated directly from an existing model. In my project, `ExperienceForm` is connected to the `Experience` model and automatically provides form fields based on the model fields, such as title, company, description, start_date, and end_date. This reduces the amount of HTML and validation logic that needs to be written manually. `ModelForm` also provides built-in validation and allows the submitted data to be saved directly to the database using `form.save()`. `{% csrf_token %}` is required to protect POST forms from Cross-Site Request Forgery (CSRF) attacks. It ensures that the POST request comes from a trusted form on my website rather than an unauthorized website attempting to perform an action using the user's session.

2. In Tutorial 03, we discussed JSON and XML data formats. Why is JSON preferred in modern web application development compared to XML?
Answer  : JSON is generally preferred in modern web applications because it has a simpler and more compact structure than XML. JSON uses a format based on objects and arrays, which makes it easy to read and work with in JavaScript and other programming languages. It also requires less syntax because it does not need opening and closing tags for every piece of data. In my project, Django serializes the Experience objects into JSON so that the data can be accessed through the `/api/experiences/` endpoint. This makes the data easier to exchange between the backend and other applications or frontend components.

3. Explain the flow that occurs when you use a view function to return your portfolio data in JSON format. Why do we need to perform the serialization process on Django models before returning the data?
Answer : When a user accesses the /api/experiences/ endpoint, Django first matches the URL with the get_experiences_json view in main/views.py. The view retrieves Experience objects from the database and converts the relevant model fields into a list of Python dictionaries. Each dictionary contains the experience ID, title, company, description, dates, star count, and whether the current user has starred the experience. The view then returns this data using JsonResponse. The conversion is necessary because Django model objects themselves are not directly JSON-compatible, while JSON-compatible data can be transmitted through HTTP and processed by JavaScript in the browser.

### Assignment 5
1. Explain the concept of debouncing and why it is important when implementing an AJAX-based search feature.
Answer  : Debouncing is a technique that delays the execution of a function until a certain amount of time has passed since the last event. In my project, the Experience search uses a 300-millisecond debounce before sending an AJAX request. Without debouncing, a request could be sent every time the user types a character, which would create many unnecessary requests while the user is still typing. Debouncing reduces the number of requests sent to the server and makes the search feature more efficient.

2. Explain the relationship between `await` and `fetch()`. What would happen if we did not use `await` when calling `fetch()`?
Answer  : `fetch()` returns a Promise because the browser needs to perform the network request asynchronously. Using `await` pauses the execution of the async function until the Promise is resolved, allowing the response to be used directly in the next step. In my project, I use `await fetch()` to wait for the server response and then use `await response.json()` to read the returned JSON data. Without `await`, the variable would contain a Promise instead of the actual response, so the code would need to handle the Promise using `.then()` or another asynchronous approach.

3. Explain what XSS is and why displaying data through JavaScript and AJAX can make XSS protection especially important.
Answer  : Cross-Site Scripting (XSS) is an attack where malicious scripts are inserted into content that is later displayed and executed in a user's browser. XSS protection is especially important when using AJAX because data returned from the server is manually inserted into the DOM using JavaScript. If untrusted data were inserted using `innerHTML`, malicious HTML or JavaScript could potentially be interpreted by the browser. In my project, the server removes HTML tags from Experience input using `strip_tags()` in the ModelForm, while the frontend uses DOM methods such as `textContent` instead of `innerHTML` when displaying the returned data. This provides protection on both the server and client sides.

### AI disclosure
I used ChatGPT as an AI-assisted learning and development tool during this assignment.
AI assistance was used to:
* explain HTML5 and CSS3 concepts used in the implementations
* help plan the HTML structure and semantic elements
* suggest CSS layouts and responsive design approaches
* explain Django MVT, ModelForm, CRUD, JSON serialization/deserialization, and CSRF concepts
* help debug and structure Django views, forms, URLs, and templates
* explain JavaScript DOM manipulation, AJAX, Fetch API, async/await, debouncing, CSRF handling, and XSS protection
* help reason through the implementation of the AJAX-based Experience section
My main prompting approach was to ask the AI to explain the reasoning behind the suggested implementations rather than only requesting a finished solution. AI-generated suggestions were not accepted blindly. I manually checked the resulting structure, corrected personal information, adjusted the implementation, and tested the functionality in the browser, including AJAX loading, search, form validation, permissions, toast notifications, and XSS protection.
