(export '(*colors*
          update-color-map
          adjust-color
          update-screen-color-context
          lookup-color))

(defvar *colors*
  '("black"
    "red"
    "green"
    "yellow"
    "blue"
    "magenta"
    "cyan"
    "white")

(defun adjust-color (color amt)
  (labels ((max-min (x y) (max 0 (min 1 (+ x y)))))
    (setf (xlib:color-red color) (max-min (xlib:color-red color) amt)
          (xlib:color-green color) (max-min (xlib:color-green color) amt)
          (xlib:color-blue color) (max-min (xlib:color-blue color) amt))))

(defun hex-to-xlib-color (color)
  (cond
   ((= 4 (length color))
    (let ((red (/ (parse-integer (subseq color 1 2) :radix 16) 255.0))
          (green (/ (parse-integer (subseq color 2 3) :radix 16) 255.0))
          (blue (/ (parse-integer (subseq color 3 4) :radix 16) 255.0)))
      (xlib:make-color :red (+ red (* 16 red))
                       :green (+ green (* 16 green))
                       :blue (+ blue (* 16 blue)))))
   ((= 7 (length color))
    (let ((red (/ (parse-integer (subseq color 1 3) :radix 16) 255.0))
          (green (/ (parse-integer (subseq color 3 5) :radix 16) 255.0))
          (blue (/ (parse-integer (subseq color 5 7) :radix 16) 255.0)))
      (xlib:make-color :red red :green green :blue blue)))))

(defun lookup-color (screen color)
  (cond
    ((typep color 'xlib:color) color)
    ((and (stringp color)
          (or (= 7 (length color))
              (= 4 (length color)))
          (char= #\# (elt color 0)))
     (hex-to-xlib-color color))
    (t (xlib:lookup-color (xlib:screen-default-colormap (screen-number screen))
                          color))))

(defun alloc-color (screen color)
  (xlib:alloc-color 
   (xlib:screen-default-colormap (screen-number screen))
   (lookup-color screen color)))

;; Normal colors are dimmed and bright colors are intensified in order
;; to more closely resemble the VGA pallet.
(defun update-color-map (screen)
  (labels ((map-colors (amt)
             (loop for c in *colors*
                   as color = (lookup-color screen c)
                   do (adjust-color color amt)
                   collect (alloc-color screen color))))
    (setf (screen-color-map-normal screen) (apply #'vector (map-colors -0.25))
          (screen-color-map-bright screen) (apply #'vector (map-colors 0.25)))))

(defun update-screen-color-context (screen)
  (let* ((cc (screen-message-cc screen))
         (bright (lookup-color screen *text-color*)))
    (setf
     (ccontext-default-fg cc) (screen-fg-color screen)
     (ccontext-default-bg cc) (screen-bg-color screen))
    (adjust-color bright 0.25)
    (setf (ccontext-default-bright cc) (alloc-color screen bright))))

;;; Parser for color strings

(defun parse-color (color)
  (if (and (> (length color) 1)
           (char= (char color 0) #\^))
      (let ((foreground (char color 1))
            (background (if (> (length color) 2)
                            (char color 2)
                            :reset)))
        (case foreground
          ;; Normalize colors
          (#\n '((:bg :reset)
                 (:fg :reset)
                 (:reverse nil)))
          (#\R '((:reverse t)))
          (#\r '((:reverse nil)))
          (#\B '((:bright t)))
          (#\b '((:bright nil)))
          (#\[ '((:push)))
          (#\] '((:pop)))
          (#\> '((:>)))
          (#\f `((:font ,(or (parse-integer (string background)
                                            :junk-allowed t)
                             0))))
          (#\^ '("^"))
          (#\( (list (read-from-string (subseq color 1))))
          ((#\0 #\1 #\2 #\3 #\4 #\5 #\6 #\7 #\8 #\9 #\*)
           `((:bg ,(or (parse-integer (string background)
                                      :junk-allowed t)
                       :reset))
             (:fg ,(or (parse-integer (string foreground)
                                      :junk-allowed t)
                       :reset))
             (:reverse nil)))))
      (list color))) ; this isn't a colorcode

(defun parse-color-string (string)
  (let ((substrings
          (remove-if
           (lambda (str) (zerop (length str)))
           (ppcre:split
            "(\\^[nrRbB>\\[\\]^]|\\^[0-9*]{1,2}|\\^f[0-9]|\\^\\(.*?\\))"
            string :with-registers-p t))))
    (loop for substring in substrings append (parse-color substring))))

(defun uncolorify (string)
  (format nil "~{~a~}" (remove-if-not 'stringp (parse-color-string string))))


;;; Color modifiers and rendering code

(defun find-color (color default cc &aux (screen (ccontext-screen cc)))
  (cond ((or (null color)
             (eq :reset color))
         default)
        ((integerp color)
         (svref (if (ccontext-brightp cc)
                    (screen-color-map-bright screen)
                    (screen-color-map-normal screen))
                color))
        (t (first (multiple-value-list (alloc-color screen color))))))

(defun find-font (cc specified-font &aux (font (or specified-font 0)))
  (if (integerp font)
      (nth font (screen-fonts (ccontext-screen cc)))
      font))

(defgeneric apply-color (ccontext modifier &rest arguments))

(defmethod apply-color ((cc ccontext) (modifier (eql :fg)) &rest args)
  (setf (ccontext-fg cc) (first args))
  (let* ((gcontext (ccontext-gc cc))
         (specified-color (first args))
         (color (find-color specified-color
                            (if (ccontext-brightp cc)
                                (ccontext-default-bright cc)
                                (ccontext-default-fg cc))
                            cc)))
    (if (ccontext-reversep cc)
        (setf (xlib:gcontext-background gcontext) color)
        (setf (xlib:gcontext-foreground gcontext) color))))

(defmethod apply-color ((cc ccontext) (modifier (eql :bg)) &rest args)
  (setf (ccontext-bg cc) (first args))
  (let* ((gcontext (ccontext-gc cc))
         (specified-color (first args))
         (color (find-color specified-color
                            (ccontext-default-bg cc)
                            cc)))
    (if (ccontext-reversep cc)
        (setf (xlib:gcontext-foreground gcontext) color)
        (setf (xlib:gcontext-background gcontext) color))))

(defmethod apply-color ((cc ccontext) (modifier (eql :reverse)) &rest args)
  (setf (ccontext-reversep cc) (first args))
  (let ((fg (ccontext-fg cc))
        (bg (ccontext-bg cc)))
    (apply-color cc :fg fg)
    (apply-color cc :bg bg)))

(defmethod apply-color ((cc ccontext) (modifier (eql :bright)) &rest args)
  (setf (ccontext-brightp cc) (first args))
  (let ((fg (ccontext-fg cc))
        (bg (ccontext-bg cc)))
    (apply-color cc :fg fg)
    (apply-color cc :bg bg)))

(defmethod apply-color ((cc ccontext) (modifier (eql :push)) &rest args)
  (declare (ignore args))
  (push (list (ccontext-fg cc)
              (ccontext-bg cc)
              (ccontext-brightp cc)
              (ccontext-reversep cc)
              (ccontext-font cc))
        (ccontext-color-stack cc)))

(defmethod apply-color ((cc ccontext) (modifier (eql :pop)) &rest args)
  (declare (ignore args))
  (let ((values (pop (ccontext-color-stack cc))))
    (apply-color cc :fg (first values))
    (apply-color cc :bg (second values))
    (apply-color cc :bright (third values))
    (apply-color cc :reverse (fourth values))
    (apply-color cc :font (fifth values))))

(defmethod apply-color ((cc ccontext) (modifier (eql :font)) &rest args)
  (let ((font (or (first args) 0)))
    (setf (ccontext-font cc) (find-font cc font))))

(defmethod apply-color ((cc ccontext) (modifier (eql :>)) &rest args)
  (declare (ignore cc modifier args)))

(defun max-font-height (parts cc)
  (font-height
   (cons (ccontext-font cc)
         (loop for part in parts
               if (and (listp part)
                       (eq :font (first part)))
                 collect (find-font cc (second part))))))

(defun reset-color-context (cc)
  (apply-color cc :fg)
  (apply-color cc :bright)
  (apply-color cc :bg)
  (apply-color cc :reverse)
  (apply-color cc :font))

(defun rendered-string-size (string-or-parts cc &optional (resetp t))
  (let* ((parts (if (stringp string-or-parts)
                    (parse-color-string string-or-parts)
                    string-or-parts))
         (height (max-font-height parts cc))
         (width 0))
    (loop
      for part in parts
      if (stringp part)
        do (incf width (text-line-width (ccontext-font cc)
                                        part
                                        :translate #'translate-id))
      else
        do (apply #'apply-color cc (first part) (rest part)))
    (if resetp (reset-color-context cc))
    (values width height)))

(defun rendered-size (strings cc)
  (loop for string in strings
        for (width line-height) = (multiple-value-list
                                   (rendered-string-size string cc nil))
        maximizing width into max-width
        summing line-height into height
        finally (progn
                  (reset-color-context cc)
                  (return (values max-width height)))))

(defun render-string (string-or-parts cc x y &aux (draw-x x))
  (let* ((parts (if (stringp string-or-parts)
                    (parse-color-string string-or-parts)
                    string-or-parts))
         (height (max-font-height parts cc)))
    (loop
       for (part . rest) on parts
       for font-height-difference = (- height
                                       (font-height (ccontext-font cc)))
       for y-to-center = (floor (/ font-height-difference 2))
       if (stringp part)
       do (draw-image-glyphs
           (ccontext-px cc)
           (ccontext-gc cc)
           (ccontext-font cc)
           draw-x (+ y y-to-center (font-ascent (ccontext-font cc)))
           part 
           :size 16)
         (incf draw-x (text-line-width (ccontext-font cc)
                                       part 
                                       :translate))
       else
       do (if (eq :> (first part))
              (progn (render-string rest cc
                                    (- (xlib:drawable-width (ccontext-px cc))
                                       x
                                       (rendered-string-size rest cc))
                                    y)
                     (loop-finish))
              (apply #'apply-color cc (first part) (rest part))))
    (values height draw-x)))

(defun render-strings (cc padx pady strings highlights)
  (let* ((gc (ccontext-gc cc))
         (xwin (ccontext-win cc))
         (px (ccontext-px cc))
         (strings (mapcar (lambda (string)
                            (if (stringp string)
                                (parse-color-string string)
                                string))
                          strings))
         (y 0))
    (when (or (not px)
              (/= (xlib:drawable-width px) (xlib:drawable-width xwin))
              (/= (xlib:drawable-height px) (xlib:drawable-height xwin)))
      (if px (xlib:free-pixmap px))
      (setf px (xlib:create-pixmap :drawable xwin
                                   :width (xlib:drawable-width xwin)
                                   :height (xlib:drawable-height xwin)
                                   :depth (xlib:drawable-depth xwin))
            (ccontext-px cc) px))
    (xlib:with-gcontext (gc :foreground (xlib:gcontext-background gc))
      (xlib:draw-rectangle px gc 0 0
                           (xlib:drawable-width px)
                           (xlib:drawable-height px) t))
    (loop for parts in strings
       for row from 0 to (length strings)
       for line-height = (max-font-height parts cc)
       if (find row highlights :test 'eql)
       do (xlib:draw-rectangle px gc 0 (+ pady y) (xlib:drawable-width px) line-height t)
         (xlib:with-gcontext (gc :foreground (xlib:gcontext-background gc)
                                 :background (xlib:gcontext-foreground gc))
           (rotatef (ccontext-default-fg cc) (ccontext-default-bg cc))
           (render-string parts cc (+ padx 0) (+ pady y))
           (rotatef (ccontext-default-fg cc) (ccontext-default-bg cc)))
       else
       do (render-string parts cc (+ padx 0) (+ pady y))
       end
       do (incf y line-height))
    (xlib:copy-area px gc 0 0
                    (xlib:drawable-width px)
                    (xlib:drawable-height px) xwin 0 0)
    (reset-color-context cc)
    (values)))
