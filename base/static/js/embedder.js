(function() {
  var Embedder = function (options) {
    // TODO:
    // features:
    // * text modification via middlewares
    // * documentation
    // * options groups
    // * common behaviour
    //
    // known issues:
    // * biding is wrong
    $.extend(this, Embedder.defaultOptions, options);

    // All works fine with an empty string, it is not necessary to throw an exception
    if (this.text === null || this.text === undefined) {
      this.text = '';
    }

    // Here we need the endpoint, so it is correct to throw the exception
    if (!this.oEmbedEndpoint) {
      throw new Error("missing option 'oEmbedEndpoint'");
    }

    if (this.autoParse) {
      this.parseAll();
    }
  };

  Embedder.noConflic = window.Embedder;
  window.Embedder = Embedder;

  Embedder.defaultOptions = {
    autoParse: true,

    commonOEmbed: function (data, callback) {
      $.ajax({
        url: this.oEmbedEndpoint + '?' + $.param(data),
        method: 'GET',
        dataType: 'json',
        success: callback,
      });
    },

    eachURL: function(pattern, func) {
      var urls = this.text.match(pattern);
      if (urls === null || urls === undefined) {
        return;
      }
      for (var i = 0, l = urls.length; i < l; i += 1) {
        if (func(urls[i]) === false) {
          break;
        }
      }
    },

    parseAll: function () {
      this.youtubeParse();
      this.vimeoParse();
    },

    vimeoCallback: $.noop,

    vimeoGetOEmbedData: function (options) {
      return {
        url: this.vimeoGetOEmbedURL(options.url),
        height: this.vimeoHeight,
        width: this.vimeoWidth,
      };
    },

    vimeoGetOEmbedURL: function (url) {
      return (
        'https://vimeo.com/api/oembed.json?url=' + encodeURIComponent(url)
      );
    },

    vimeoHeight: null,

    vimeoOEmbed: function (url) {
      this.commonOEmbed(
        this.vimeoGetOEmbedData({ url: url }),
        this.vimeoCallback,
      );
    },

    vimeoParse: function () {
      this.eachURL(this.vimeoPattern, this.vimeoOEmbed);
    },

    vimeoPattern: new RegExp(
      '(?:https?:\\/\\/)?(?:www\\.|player\\.)?' +
      '(vimeo\\.com\\/)' +
      '(?:([\\w]+)\\/?)*',
      'g'
    ),

    youtubeCallback: $.noop,

    youtubeGetOEmbedData: function (options) {
      return {
        url: this.youtubeGetOEmbedURL(options.url),
      };
    },

    youtubeGetOEmbedURL: function (url) {
      return (
        'https://www.youtube.com/oembed?url=' + encodeURIComponent(url) +
        '&format=json'
      );
    },

    youtubeOEmbed: function (url) {
      this.commonOEmbed(
        this.youtubeGetOEmbedData({ url: url }),
        this.youtubeCallback
      );
    },

    youtubeParse: function () {
      this.eachURL(this.youtubePattern, this.youtubeOEmbed);
    },

    youtubePattern: new RegExp(
      '(?:https?:\\/\\/)?(?:www\\.)?' +
      '(youtube\\.com\\/|youtu\\.be\\/)' +
      '([\\w_-]+)(?:\\/)?' +
      '([\\w?&=_-]+)?',
      'g'
    ),
  };
})();
