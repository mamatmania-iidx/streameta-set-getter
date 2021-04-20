**Features**
* Grabs player names from your Streameta overlay and displays their recent matches.
* Supports Smash.GG brackets (Other bracket sites coming soon)

**Limitations**
Currently only works with Smash.GG, Challonge support coming soon.
*Only supports bracket links to event, not tournament.*
May still have bugs w.r.t. Players with no games played.

**How to use**
1. Clone the project, and install dependencies from requirements.txt.
2. Create .env file, and fill it it with your [Smash.GG API key](https://developer.smash.gg/docs/authentication/) and [Streameta token](https://streameta.com/help/#8.5).
3. Run main.py.
4. Add p1_sets.txt and p2_sets.txt to your OBS/Xsplit scene where necessary.