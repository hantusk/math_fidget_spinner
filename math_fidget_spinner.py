# %%
from build123d import *
from bd_warehouse.gear import SpurGear
import jupyter_cadquery
import random

fidget_spinner_disc_radius = 90 * MM / 2
fidget_spinner_top_button_radius = fidget_spinner_disc_radius / 2
num_numbers = 15
def math_function(x):
    """4x"""
    return 4*x
input_numbers = random.sample(range(8, 32), num_numbers)

# %%
text_baseline_radius = fidget_spinner_disc_radius * 0.775
tolerance = 0.0
font_path="Hind-Bold.ttf"

# %%
with BuildPart() as fidget_spinner_button_top:
    with BuildSketch() as s:
        Circle(fidget_spinner_top_button_radius)
    extrude(amount=2)
    chamfer(
        fidget_spinner_button_top.edges()
        .filter_by(GeomType.CIRCLE)
        .sort_by(SortBy.RADIUS)
        .sort_by(Axis.Z)[0],
        angle=45,
        length=0.5,
    )

    top_face = fidget_spinner_button_top.faces().sort_by(Axis.Z)[-1]
    with BuildSketch(top_face) as s:
        bearing_bore_radius = (8 - tolerance) / 2
        Circle(bearing_bore_radius)
    extrude(amount=4)
    chamfer(
        fidget_spinner_button_top.edges()
        .filter_by(GeomType.CIRCLE)
        .sort_by(SortBy.RADIUS)
        .sort_by(Axis.Z)[-1],
        angle=45,
        length=0.25,
    )

    with BuildSketch(top_face) as s:
        bearing_bore_case_radius = 12 / 2
        Circle(bearing_bore_case_radius)
    extrude(amount=1)

    bottom_face = fidget_spinner_button_top.faces().sort_by(Axis.Z)[0]
    with BuildSketch(bottom_face) as fidget_spinner_button_text:
        with Locations((0, -0.53*fidget_spinner_top_button_radius)):
            Text(
                math_function.__doc__,
                font_size=fidget_spinner_top_button_radius * 0.4,
                font_style=FontStyle.BOLD,
                font_path=font_path
            )
    extrude(amount=-0.4, mode=Mode.SUBTRACT)
    extrude(
        to_extrude=(
            import_svg("arrow.svg")[0]
            .translate((-24, -24))
            .scale(fidget_spinner_top_button_radius*0.02)
            .rotate(Axis.Z, 180)
            .translate((0, -0.53*fidget_spinner_top_button_radius))
        ),
        amount=0.4,
        mode=Mode.SUBTRACT,
    )

    export_step(fidget_spinner_button_top.part, "fidget_spinner_button_top.step")
fidget_spinner_button_top.part

# %%
with BuildPart() as fidget_spinner_disc:
    gear = SpurGear(
        module=fidget_spinner_disc_radius*2/num_numbers,
        tooth_count=num_numbers,
        pressure_angle=18,
        root_fillet=0.25 * MM,
        thickness=2.5 * MM,
        addendum=0,
    )

    # Gear is very slow to generate. Uncomment this section to use a disc as a placeholder while debugging, and comment out the gear code above.
    # with BuildPart() as placeholder_disc:
    #     with BuildSketch() as placeholder_circle:
    #         Circle(fidget_spinner_disc_radius)
    #     extrude(amount=2.5 * MM)
    # gear = placeholder_disc.part

    fidget_spinner_disc.part = fidget_spinner_disc.part + gear
    fillet(
        fidget_spinner_disc.faces().sort_by(Axis.Z)[-1].edges(),
        radius=1 * MM,
    )
    chamfer(
        fidget_spinner_disc.faces().sort_by(Axis.Z)[0].edges(),
        angle=45,
        length=0.9 * MM,
    )

    with BuildSketch() as center_hole:
        Circle((22 * MM + tolerance) / 2)
    extrude(amount=6 * MM, mode=Mode.SUBTRACT, both=True)
    fillet(
        fidget_spinner_disc.faces()
        .sort_by(Axis.Z)[-1]
        .edges()
        .filter_by(GeomType.CIRCLE),
        radius=0.25 * MM,
    )

    top_face_of_disc = fidget_spinner_disc.faces().sort_by(Axis.Z)[-1]
    bottom_face_of_disc = fidget_spinner_disc.faces().sort_by(Axis.Z)[0]
    with BuildSketch(top_face_of_disc) as numbers:
        for index, number in enumerate(input_numbers):
            with PolarLocations(
                text_baseline_radius,
                1,
                -index * 360 / num_numbers + 90,
                360,
                rotate=True,
            ):
                Text(
                    str(number),
                    font_size=text_baseline_radius * 0.2,
                    font_style=FontStyle.BOLD,
                    rotation=-90,
                    font_path=font_path,
                )
    extrude(amount=0.2)

    with BuildSketch(bottom_face_of_disc) as answers:
        for index, number in enumerate(input_numbers):
            with PolarLocations(
                text_baseline_radius, 1, index * 360 / num_numbers - 90, 360, rotate=True
            ):
                Text(
                    str(math_function(number)),
                    font_size=text_baseline_radius * 0.2,
                    font_style=FontStyle.BOLD,
                    rotation=90,
                    font_path=font_path,
                )
    extrude(amount=-0.4, mode=Mode.SUBTRACT)
export_step(fidget_spinner_disc.part, 'fidget_spinner_disc.step')
fidget_spinner_disc.part

# %%
# Ideas for other operators
operators = [
    "add",
    "subtract",
    "multiply",
    "divide",
    "percentage",
    "power",
    "root",
    "triangle_angle_difference",
    "pythoragoras",
]

# %%



