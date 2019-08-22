lint:
	docker run --rm --env-file=.lint -v "$(CURDIR)":/app divio/lint /bin/lint ${ARGS}
