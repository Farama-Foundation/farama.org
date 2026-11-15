Repo for the source code for farama.org

## Setup

Install [mise](https://mise.jdx.dev/), then from the repo root:

```
mise install
bundle install
```

This installs Ruby, `just`, and `bundler` (via the `mise postinstall` hook), then the Jekyll gems.

## Serving locally

Serve on the local network (accessible from phone):
```
just serve
```

Find your IP:
```
just find-local-ip
```
Then open `http://<your-ip>:4000` on the other device.

## Shared docs header

Every Farama documentation site loads [`assets/docs/shared.js`](assets/docs/shared.js) from farama.org on each page view, including on archived docs versions. It builds the Farama project menu from [`api/projects.json`](api/projects.json) (generated from [`_data/projects.yml`](_data/projects.yml)) and loads the December fundraising banner in [`assets/fundraising`](assets/fundraising).

A change to any of these is live on all docs sites as soon as this site deploys, with no docs rebuild. Keep the script dependency free and tolerant of old page markup, since it also runs on docs built years ago.

## Built with

* Jekyll
* Bootstrap 5
* Font Awesome
