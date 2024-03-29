---
layout: default
title: Side Icon
parent: Experimental
has_children: false
nav_order: 6
---

# Side Icon (Modified)

Based on the original IconSide class


```
class IconSide(Icon):  # modified Representation IconSide class 
    def __init__(self, config: dict, button: "Button"):
        config['icon-color'] = config['side'].get("icon-color", button.get_attribute("default-icon-color"))
        Icon.__init__(self, config=config, button=button)

        self.side = config.get("side")  # multi-labels
        self.centers = self.side.get("centers", [43, 150, 227])  # type: ignore
        self.labels: str | None = self.side.get("labels")  # type: ignore
        self.label_position = config.get("label-position", "cm")  # "centered" on middle of side image

    def get_datarefs(self):
        datarefs = []
        for label in self.labels:
            drefs = self.button.scan_datarefs(label)
            if len(drefs) > 0:
                datarefs = datarefs + drefs
        return datarefs

    # def get_datarefs(self):
    #     if self.datarefs is None:
    #         self.datarefs = []
    #         if self.labels is not None:
    #             for label in self.labels:
    #                 dref = label.get('dataref')
    #                 if dref is not None:
    #                     logger.debug(f"button {self.button_name()}: added label dataref {dref}")
    #                     self.datarefs.append(dref)
    #     return self.datarefs

    def is_valid(self):
        if self.button.index not in ["left", "right"]:
            logger.debug(f"button {self.button_name()}: {type(self).__name__}: not a valid index {self.button.index}")
            return False
        return super().is_valid()

    def get_image_for_icon(self):
        """
        Helper function to get button image and overlay label on top of it for SIDE keys (60x270).
        Side keys can have 3 labels placed in front of each knob.
        (Currently those labels are static only. Working to make them dynamic.)
        """
        image = super().get_image_for_icon()

        if image is None:
            return None

        draw = None

        if self.labels is not None:
            image = image.copy()  # we will add text over it
            draw = ImageDraw.Draw(image)
            inside = round(0.04 * image.width + 0.5)
            vheight = 38 - inside

            vcenter = [35, 124, 213]  # this determines the number of acceptable labels, organized vertically
            cnt = self.side.get("centers")

            if cnt is not None:
                vcenter = [round(270 * i / 100, 0) for i in convert_color(cnt)]  # !

            li = 0
            for label in self.labels:
                txt = label.get("label")

                get_text = self.button.get_text(label, root="text")

                if li >= len(vcenter) or txt is None:
                    continue

                txto = get_text

                lfont = label.get("label-font", self.label_font)
                lsize = label.get("label-size", self.label_size)
                font = self.get_font(lfont, lsize)

                # Horizontal centering is not an issue...
                label_position = label.get("label-position", self.label_position)
                w = image.width / 2
                p = "m"
                a = "center"
                if label_position == "l":
                    w = inside
                    p = "l"
                    a = "left"
                elif label_position == "r":
                    w = image.width - inside
                    p = "r"
                    a = "right"
                # Vertical centering is black magic...
                h = vcenter[li] - lsize / 2
                if label_position[1] == "t":
                    h = vcenter[li] - vheight
                elif label_position[1] == "b":
                    h = vcenter[li] + vheight - lsize

                draw.multiline_text(
                    (w, h), text=txt, font=font, anchor=p + "m", align=a, fill=label.get("label-color", self.label_color)  # (image.width / 2, 15)
                )

                # Text below LABEL
                tfont = label.get("text-font")
                tsize = label.get("text-size")
                tfont = self.get_font(tfont, tsize)

                text_position = h + lsize + 5  # Adjust based on your needs, adding lsize for simplicity
                draw.text(
                    (w, text_position), text=txto, font=tfont, anchor=p + "m", align=a, fill=label.get("text-color")
                )

                li = li + 1
        return image

    def describe(self):
        return "The representation produces an icon with optional label overlay for larger side buttons on LoupedeckLive."

```