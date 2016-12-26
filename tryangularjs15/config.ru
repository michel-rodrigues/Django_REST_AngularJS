use Rack::Static,
    :urls => ["/img", "/js", "/css", "/templates", "/json"],
    :root => "source"

run lambda { |env|
    [
        200,
        {
            'Content-Type'  => 'text/html',
            'Cache-Control' => 'public, max-age=86400'
        },
        File.open('source/index.html', File::RDONLY)
    ]
}
