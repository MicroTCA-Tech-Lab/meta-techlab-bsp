
# This patch removes a FIFO in case there is no monitor (framebuffer) present.
# When there is no monitor present, the FIFO is not read and blocks
# /etc/init.d/rc script which would like to communicate the progress of the
# boot process over this FIFO

python do_patch_append() {

    PATCH_STR = """Index: psplash-init
===================================================================
--- psplash-init
+++ psplash-init
@@ -10,6 +10,8 @@
 if [ ! -e /dev/fb0 ]; then
     echo \"Framebuffer /dev/fb0 not detected\"
     echo \"Boot splashscreen disabled\"
+    echo \"FIX: removing splashscreen FIFO\"
+    rm -f /mnt/.psplash/psplash_fifo
     exit 0;
 fi
"""

    import subprocess
    p = subprocess.Popen(["patch", "-b"], stdin=subprocess.PIPE)
    p.communicate(input=PATCH_STR.encode("ascii"))
}

