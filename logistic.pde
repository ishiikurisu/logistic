final color WHITE = #FFFFFF;
final color BLACK = #000000;
float left = 0.0;
float right = 4.0;
String state = "idle";
float memory = 0;

boolean is_in(FloatList l, float x) {
    return l.hasValue(x);
}

float[] logistic_map(float x, float r) {
    FloatList stable_points = new FloatList();

    // stabilizing
    for (int i = 0; i < 2400; i++) {
        x = r * x * (1-x);
    }

    // picking stable points
    for (int i = 0; i < 1000; i++) {
        x = r * x * (1-x);
        if (!is_in(stable_points, x)) {
            stable_points.append(x);
        }
    }

    return stable_points.array();
}

void draw_map() {
    float step = (right - left)/width;
    float r = left;

    background(BLACK);
    noStroke();
    fill(WHITE);
    for (int x = 0; x < width; x++) {
        float[] points = logistic_map(0.5, r);
        for (int j = 0; j < points.length; j++) {
            float point = points[j];
            float y = height * (1-point);
            ellipse(x, y, 2, 2);
        }
        r += step;
    }
}

void setup() {
    size(1000, 600, P2D);
    println("drawing...");
    draw_map();
    println("drawn");
}

void draw() {

}

void keyPressed() {
    switch (key) {
        case 'f':
        case 'F':
            if (state == "idle") {
                memory = (right - left) * float(mouseX) / float(width) + left;
                state = "waiting";
            } else if (state == "waiting") {
                println(memory);
                left = memory;
                right = 4;
                draw_map();
                state = "idle";
            }
        break;

        case 't':
        case 'T':
            if (state == "waiting") {
                right = (right - left) * float(mouseX) / float(width) + left;
                left = memory;
                if (left > right) {
                    memory = right;
                    right = left;
                    left = memory;
                }
                draw_map();
                state = "idle";
            }
        break;

        case 'r':
        case 'R':
            left = 0;
            right = 4;
            draw_map();
            state = "idle";
        break;
    }
}
