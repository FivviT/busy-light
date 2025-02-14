TODO:

* Create simple web server that serves web page with next functionality:
  * Turn on/off led
  * Set brightness
  * Set color for each led separately or for all
  * Show connected calendars
  * Add/remove calendar
* Create kind a cron job that refresh meetings data from Google calendar every 10-20 minutes. Blink with some specific colour when can't retrieve data from GC.
* Create worker that turn on led ring when meeting start and turn off it when meeting is over. Bonus: light led as progress bar depends on how many time left for meeting.
* Next data should be stored locally in file:
  * LED config (color, brightness)
  * Google tokens to refresh calendars
  * WI-FI user/password
  * Meetings Time intervals (probably separate file)
* Create webpage that will be server on Access Point web server to set up WI-FI user/password
* Find a way how to add DNS to router to server page on specific host
