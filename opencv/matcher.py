import cv2



class Matcher:
    def __init__(self, templates, mininum_matches  = 25):
        FLANN_INDEX_KDTREE = 0
        # set min matches required to confirm template was detected
        self.minimum_matches = mininum_matches

        # create SIFT object features extractor
        self.sift = cv2.xfeatures2d.SIFT_create()
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)

        # create object matcher
        self.flann = cv2.FlannBasedMatcher(index_params, search_params)

        self.descriptors = {}
        for (label, filename) in templates:
            img = cv2.imread(filename, 0)
            print "Label = %s, Filename = %s" % (label, filename)
            kp, des = self.sift.detectAndCompute(img, None)
            self.descriptors[label] = des


    def match(self, img):
        imgk, imgdes = self.sift.detectAndCompute(img, None)

        max_matches = 0
        detected_label = None

        for label, des in self.descriptors.items():
            matches = self.flann.knnMatch(des, imgdes, k=2)

            ## store all the good matches as per Lowe's ratio test.
            cnt = 0
            for m, n in matches:
                if m.distance < 0.7 * n.distance:
                    cnt = cnt + 1
            print "Found %s matches for %s" % (cnt, label)

            if cnt > self.minimum_matches and cnt > max_matches:
                max_matches = cnt
                detected_label = label


        return detected_label