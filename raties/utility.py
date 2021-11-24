import pysftp, os


def sftp_connection():
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    folder = os.getenv("SFTP_FOLDER")
    if int(os.getenv("SFTP_KEY_PASS_ENABLE")) == 1 :
        if os.getenv("SFTP_KEY_PASS") == "":
            srv = pysftp.Connection(os.getenv("SFTP_SERVER"), username=os.getenv("SFTP_USERNAME"),
                                    private_key=os.getenv("SFTP_PRIVATE_KEY"), cnopts=cnopts)
        else:

            srv = pysftp.Connection(os.getenv("SFTP_SERVER"), username=os.getenv("SFTP_USERNAME"),
                                    private_key_pass=os.getenv("SFTP_KEY_PASS"),
                                    private_key=os.getenv("SFTP_PRIVATE_KEY"), cnopts=cnopts)

    else:
        print("passowrd")
        srv = pysftp.Connection(os.getenv("SFTP_SERVER"), username=os.getenv("SFTP_USERNAME"),
                                password=os.getenv("SFTP_PASSWORD"), cnopts=cnopts)

    return srv
    # srv.cwd(folder)
    # print("start")
    # srv.put("442-.pdf","document/"+"442-.pdf")
    # print("done")
