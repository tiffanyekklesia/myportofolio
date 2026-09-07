Name    : Tiffany

NPM     : 2506546062

Class   : PBP E

### Assignmnet 1
1. In Tutorial 1 and Individual Assignment 1, you were given the freedom to decide your portfolio website’s design. When you designed the HTML structure you used, did you use semantic HTML5 elements such as <section>, <article>, or <aside>? If so, how did those elements help you build the static web? If not, why did your design’s needs stay met without them?
Answer: I used semantic HTML5 elements in my portofolio. I used <section> to separate major parts of the page, such as the About Me, Projects, and Skills sections. Within the projects and Skills sections, I used <article> to represent individual pieces of content. This made the HTML structure easier to understand and maintain because the structure of the page reflects the meaning of its content rather than only its visual appearance. I also used <nav> for the navigation links and <footer> for the information at the bottom of the page.

2. When you set up your CSS to stay responsive, what layout challenges did you encounter? How did you evaluate which elements needed to be repositioned or prioritized in size when moving from the desktop view to mobile?
One of the main challenges was maintaining the two-column layout of the About Me section while keeping the profile photo and text readable on smaller screens. I used CSS Grid for the desktop layout and changed it into a single column layout through media queries on smaller screens. I also changed the Projects grid from three columns into one column on smaller screens. I prioritized the profile information,photo, and navigation because they are the most important elements of the page. I evaluated the layoyt by testing teh website at different browser widths and checking whether text became crowded, elements overflowed, or buttons and navigation links becmae difficult to use.

3. The website you’ve built right now is a purely static web. What limitations did you feel while trying to present your portfolio’s information optimally? Based on those limitations, what dynamic functionality would you most want to prepare and add in the next iteration of the project?
The main limitation of a static website is that the content has to be edited directly on the HTML files. For example, adding a new project or updating infomration requires manually changing the source code. A dynamic version could store projects and personal information in a database so that the content could be managed without directly editing the HTML. In thenext iteration, I would like to add dynamic project section where projects can be stored, updated, an ddisplayed using Django's MVT architecture.

### AI disclosure
I used ChatGPT as an AI-assisted learning and development tool during this assigment.

AI assistance was used to:
- explain HTML5 and CSS3 concepts used in the implementations
- help plan the HTML structure and semantic elements
- suggest CSS layouts and responsive design approaches
My main prompting approach was to ask the AI to explain the reasoning behind the suggested HTML and CSS rather than only requesting a finished solution. AI-generated suggestions were not accepted blindly. I manually checked the resulting structure, corrected personal information, adjusted the layout, and tested the implemenattion in the browser.