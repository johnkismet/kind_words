# Kind Words

A Slack bot for writing kind letters to real people. Write and receive encouraging letters throughout the day. Trade stickers and listen to music with your coworkers. We're all in this together, sometimes all you need are a few kind words.

## How will users interact with the bot?

Ideally we will streamline interaction to be button based, rather than using commands. The MVP may have to rely on commands, though.
There are 4 interactions a user can make: 

### Send Kind Words
Users can write kind words, letters of encouragement, quotes, gratitudes, or anything positive here. All of these will be posted to a slack channel anonymously.
### Make a Request
A request is an anonymous message sent for everyone to see and respond to, if they choose. The author may ask for advice, thoughts, words of encouragment, and other things along those lines. Only the poster can see the responses, but everything is anonymous (unless people choose to include their name in their message)
### View Requests
This is where users can go to read other requests, and respond if they choose. All submissions are anonymous, unless the user chooses to include their name.
### View Stickers
This is exciting to me. We will have a small economy of stickers, there's so much creativity possible. Users can send stickers when responding to a request (so the request author receives the sticker), and as a thank you to responses on their own request. They can only send stickers that they own, so we will have to implement a dropdown box that populates with the available stickers

## The Sticker Economy
- Each user starts with 1 random sticker. 
- They can send that whenever responding to a request or as a thank you to responses they get.
- This is how the economy of stickers works, each user trades and gets gifted stickers blindly.
- They may already own the sticker, in that case nothing happens.
- The stickers are just a fun collectible aspect.
- We can try to use the Wunderkind characters at first, and add on eventually.

## Privacy
I believe that while this project is contained to Wunderkind we should avoid tracking the authors of requests/responses. But this is up for discussion, maybe it's best we play it safe and include a reporting system early (which would require logging the authors of requests, responses, and kind words)
## Backlog Ideas
- Create a live WKND jukebox that employees can tune into throughout the work day. the songs in the playlist are added by submissions from employees
