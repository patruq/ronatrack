FROM node:latest

WORKDIR /app

COPY ./react/ronatrack /app

RUN yarn install

ENV PATH ./node_modules/.bin/:$PATH

COPY ./compose/local/react/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start


COPY ./compose/local/react/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint


ENTRYPOINT ["/entrypoint"]
