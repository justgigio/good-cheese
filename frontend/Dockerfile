FROM oven/bun:1.0.27-slim as base
WORKDIR /app

FROM base AS install
RUN mkdir -p /temp/dev
COPY package.json bun.lockb /temp/dev/
RUN cd /temp/dev && bun install --frozen-lockfile

FROM base AS dev
COPY --from=install /temp/dev/node_modules node_modules
COPY . ./

EXPOSE 8888/tcp
CMD [ "bun", "run", "dev" ]
