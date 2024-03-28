# Environment variables

There's a `.env.template` file that is the source of truth for
environment variable keys. You're supposed to create a `.env.local` file
and a `.env.prod` file based on `.env.template`. The keys in each
environment variable file should stay the same at all times. This is
enforced programmatically using Invoke tasks. (See the `tasks.py` file
for more details on this.) The values of the keys can differ between
files, of course.

When you deploy to production, the production environment variables are
automatically uploaded to production.
