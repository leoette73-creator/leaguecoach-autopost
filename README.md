# League Coach autopost

Posts **5 reels at 6 am, 5 at 12 pm and 5 at 6 pm** Sydney time (an hour later in winter) to **@leaguecoach.au**, in the order listed in `posts.json`. Each run picks the next reel that isn't in `posted.json`, posts it with its caption, and records it.

## One-time setup (about 15 minutes)

### 1. Make your Instagram a professional account
Instagram app → your profile → ☰ → **Account type and tools** → **Switch to professional account** (Creator is fine). It's free.

### 2. Get an Instagram access token
1. Go to **developers.facebook.com** and log in. Click **My Apps → Create app**.
2. Choose the use case **"Manage messaging & content on Instagram"**, give it any name (e.g. "League Coach Autopost") and create it.
3. In the app, open **Instagram → API setup with Instagram login**.
4. Under **Generate access tokens**, click **Add account**, log in with @leaguecoach.au and allow access.
5. Click **Generate token** and copy it. It's a long string. Keep it private, like a password.

The app can stay in development mode because it only posts to your own account.

### 3. Put this folder on GitHub
The easiest way is **GitHub Desktop** (desktop.github.com):
1. Open GitHub Desktop and sign in → **File → Add local repository** → pick this `leaguecoach-autopost` folder → **create a repository** when it asks.
2. Click **Publish repository**. **Untick "Keep this code private"**, because Instagram has to be able to download the videos from it.

### 4. Turn on the daily schedule
On github.com open the repo → **Add file → Create new file**.
- Name it exactly: `.github/workflows/post.yml`
- Open `workflow_post.yml` from this folder, copy everything, and paste it in.
- Click **Commit changes**.

### 5. Add the token to GitHub
On github.com open the repo → **Settings → Secrets and variables → Actions → New repository secret**
- Name: `IG_ACCESS_TOKEN`
- Secret: paste the token from step 2

### 6. Test it
Repo → **Actions** tab → **Post next reel** → **Run workflow**. Within a few minutes the first reel should be on your Instagram, and `posted.json` will update. After that it runs by itself every day.

## Every 60 days
Instagram tokens expire after 60 days. Generate a new one (step 2.4–2.5) and paste it into the `IG_ACCESS_TOKEN` secret (step 5).

## Adding more reels
Drop the new `.mp4` into `videos/`, add an entry to the end of `posts.json` with its file name and caption, then commit and push in GitHub Desktop.

## Changing how many get posted
In `.github/workflows/post.yml`, change `POSTS_PER_RUN` (reels per time slot) or delete one of the `cron` lines to drop a time slot.

## Pausing
Actions tab → **Post next reel** → **⋯ → Disable workflow**.
