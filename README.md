# Handover guide

## How to create a Custom Amazon Skill
Requirements: Amazon Developer Account

NB You have been granted administrator role for the existing beta skill.

1. Log in to your Amazon Developer account. 
2. Open Amazon Alexa Developer console (https://developer.amazon.com/alexa/console/ask).
3. Click 'Create Skill' (blue button).
4. Enter skill name (this cannot be changed later) and pick default language.
5. Pick Custom model and Alex-hosted (Python) backend.
6. Import skill from public git repo.

## How to use custom lambda with your Skill
Requirements: Amazon Developer Account, Custom Amazon Skill with backend in Python
1. Log in to your Amazon Developer account. 
2. Open Amazon Alexa Developer console.
3. Copy Skill ID from the skill you want to connect.
4. In a new tab open AWS Developer Centre.
5. On the nav bar go to Products > Serverless > AWS Lambda.
6. Click 'Get started with AWS Lambda', and then Create Function (orange button on the right).
7. On the next screen, choose 'Author from scratch', type in function name (this is NOT the name of the file, just the name of the Amazon Lambda), and choose runtime (we used Python 3.7).
8. If you haven't used AWS Lambda before, for 'Execution role' pick 'Create a new role with basic Lambda permissions'. Otherwise you can choose an existing role. Keep in mind the rule of least privilige access.
9. Click 'Create function' (orange button, bottom right).
10. In 'Code source' panel, pick 'Upload from .zip files' and upload the zip folder  NAMEHERE we sent you.
11. Deploy changes.
12. In 'Function overview' on top click 'Add trigger'
13. For 'Trigger configuration' choose Alexa Skills Kit.
14. For 'Skill ID verification' pick Enable and paste the Skill ID of your custom skill. Add the trigger (orange button, bottom right).
15. From 'Function overview' copy function ARN. It has a format of region:unique_id:function:name_of_your_lambda.
16. Move to Amazon Alexa Developer Console and open your skill.
17. On the left panel click 'Endpoint'.
18. Delete the content of 'Deafault region box' anc paste the function ARN from point 15.
19. Save endpoints (button with blue text on top of the page).
20. Test the skill to check the connections.

## How to use SSML tags
Here is an example of a skill output using ssml. 
```python
        speak_output = '<speak> \
                        <voice name="Matthew"> \
			<amazon:domain name="conversational"> \
                        Hello! My name is Alfred. \
                        </amazon:domain>
			</voice> \
                        </speak>'              
```
Be careful to use different quotes inside the tags than what you're using for the whole output.


## Follow up on your questions from the presentation
Making the skill more conversational
* Amazon Lex will help you with the _content_ of the output 
	https://aws.amazon.com/lex/
* SSML Conversational style and Alexa Conversations will help you with _how_ the content is said, i.e. making it sound more human-like
  	https://developer.amazon.com/en-US/docs/alexa/conversations/about-alexa-conversations.html

Including an intervention (memory training) as a part of your skill - systematic review:
* M. Dugas, G. Gao and R. Agarwal, "Unpacking mHealth interventions: A systematic review of behavior change techniques used in randomized controlled trials assessing mHealth effectiveness", DIGITAL HEALTH, vol. 6, pp. 1-16, 2020. 

## Other resources 
ASK CLI
* https://developer.amazon.com/en-US/docs/alexa/smapi/quick-start-alexa-skills-kit-command-line-interface.html

CI/CD rom https://github.com/alexa/alexa-skills-kit-sdk-for-python
* Unit tests https://github.com/alexa/alexa-skills-kit-sdk-for-python/tree/master/ask-sdk-core/tests/unit
* Local debugging https://github.com/alexa/alexa-skills-kit-sdk-for-python/tree/master/ask-sdk-local-debug

Skill certification
* https://developer.amazon.com/en-US/docs/alexa/custom-skills/certification-requirements-for-custom-skills.html


