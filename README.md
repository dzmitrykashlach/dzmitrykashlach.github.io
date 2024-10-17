# Dzmitry Kashlach - Personal Website

A Jekyll-based personal website and blog, hosted on GitHub Pages.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Ruby** (version 2.7 or higher recommended)
- **RubyGems** (usually comes with Ruby)
- **Bundler** gem

To check if you have these installed:

```bash
ruby --version
gem --version
bundle --version
```

If Bundler is not installed, install it with:

```bash
gem install bundler
```

## Installation

1. Clone this repository:

```bash
git clone https://github.com/dzmitrykashlach/dzmitrykashlach.github.io.git
cd dzmitrykashlach.github.io
```

2. Install dependencies:

```bash
bundle install
```

This will install all required gems specified in the `Gemfile`, including Jekyll and GitHub Pages.

## Running Locally in Development Mode

To start the Jekyll development server with auto-reload:

```bash
bundle exec jekyll serve
```

Or for more verbose output:

```bash
bundle exec jekyll serve --verbose
```

The site will be available at `http://localhost:4000` by default.

### Development Server Options

- **Auto-reload on file changes**: Enabled by default
- **Draft posts**: Include drafts with `--draft` flag
- **Future posts**: Include future-dated posts with `--future` flag
- **Force rebuild**: Use `--force_polling` on some file systems
- **Specify port**: Use `--port 4001` to use a different port
- **Specify host**: Use `--host 0.0.0.0` to make it accessible on your network

Example with options:

```bash
bundle exec jekyll serve --draft --future --host 0.0.0.0 --port 4000
```

## Building for Production

To build the site without running a server:

```bash
bundle exec jekyll build
```

The output will be in the `_site` directory. This directory is typically git-ignored.

## Troubleshooting

### Port Already in Use

If port 4000 is already in use, specify a different port:

```bash
bundle exec jekyll serve --port 4001
```

### Permission Errors

If you encounter permission errors during `bundle install`, you may need to install gems for your user only:

```bash
bundle install --path vendor/bundle
```

### Dependency Issues

If you experience dependency conflicts, try:

```bash
bundle update
```

Or reset your dependencies:

```bash
rm Gemfile.lock
bundle install
```

### Windows Issues

On Windows, you may need to install the `wdm` gem separately or use `--force_polling`:

```bash
bundle exec jekyll serve --force_polling
```

## Project Structure

- `_config.yml`: Jekyll configuration
- `_posts/`: Blog posts (markdown files with date prefix)
- `_site/`: Generated site (git-ignored, do not edit manually)
- `resume_en.markdown` / `resume_ru.markdown`: Resume pages
- `index.markdown`: Homepage
- `Gemfile`: Ruby dependencies

## Updating Dependencies

To update all gems to their latest compatible versions:

```bash
bundle update
```

To update specific gems:

```bash
bundle update github-pages
```

## Additional Resources

- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Minima Theme](https://github.com/jekyll/minima)

## License

This project is a personal website. All content is copyright of the respective authors.
