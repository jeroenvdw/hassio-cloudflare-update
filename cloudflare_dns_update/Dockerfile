ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements for add-on
RUN \
  apk add --no-cache \
    python3

# Copy data for add-on
COPY update_dns_record.py /
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]