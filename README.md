# Amazon_products
in the project we are going to extract product information from amazon.it is not possible using requests
because the amazon  block scrapers using the following technique like
IP Blocking / Rate Limiting,User-Agent Detection,Header Validation,CAPTCHA Challenges,JavaScript Challenges
Dynamic Page Content,Geo-blocking / Location-Based Restrictions,Session / Cookie Checks,Login Requirement
Honeypot Links,Click / Scroll Behavior Detection,Frequent DOM/Class Changes,TLS Fingerprinting,Request Frequency
Pattern Analysis,Behavioral Analysis (AI/ML)
so we decided to use playwright which is  a modern tool alternative to selenium but faster and advance then selenium .
we extracted the data using playwright and letter on parse it using beautiful soup and extracted required data
and save it to the Google sheets using google sheets api.
