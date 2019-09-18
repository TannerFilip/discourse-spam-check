# discourse-spam-check

**USE THIS SCRIPT AT YOUR OWN RISK.**

**v0.5.0**

A script to run through the "suspect" and "silenced" users list to check for spam accounts. 


## Install

* **Requirements**: Tested on Python 3.6, needs `requests` and `colorama`. 

1. `pip install -r requirements.txt`
2. `cp config.example.py config.py`
3. Set constants in config.py. You can probably skip `USERNAME_OVERRIDE`. That's mostly a workaround for Mozilla's site.
## Usage


```
$ python main.py -h

usage: Discourse Spam Checker [-h] [--type {all,suspect,silenced}]                                                      
optional arguments:
  -h, --help            show this help message and exit
  --type {all,suspect,silenced}, -t {all,suspect,silenced}
                        Specify which user list to scan. Defaults to 'all'
```

To run only on `suspect`:
`python main.py -t suspect`, same deal for `silenced` and `all`. If nothing is specified, it'll default to all

Example: 

```
Found user: SpammerMcSpamFace
User ID: 127001
User bio:
I'm just a spammer with a bunch of spam here.
Silenced by system
Reason: New user typed too fast
What would you like to do?
[S]kip, [d]elete and block IP, [o]pen in browser, [q]uit
> : d
Really delete heenakhanbang? There is no undo!
Type 'y' and press return to delete.
> y
Deleted SpammerMcSpamFace

```

All you do is press "d", and then "y". All their posts are now deleted, and their email, IP, and any URLs they had are now blocked.

Hitting enter/return before entering anything else just skips the user.

## Roadmap

* User whitelist
* Dry-run
* ???


## Disclaimer


I've used this on a production site with tens of thousands of users and haven't had any problems. 
That said, it's possible (likely) I've made mistakes in this program. I encourage you to look at the source for yourself first.

As the MIT [LICENSE](LICENSE) so eloquently puts it:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
