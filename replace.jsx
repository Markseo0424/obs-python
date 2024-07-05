{
    function replaceSliderExpressions() {
        var comp = app.project.activeItem; // 현재 활성화된 컴포지션을 가져옵니다.

        if (comp == null || !(comp instanceof CompItem)) {
            alert("Please select a composition.");
            return;
        }

        app.beginUndoGroup("Replace Slider Expressions"); // 실행 취소 그룹 시작

        for (var i = 1; i <= comp.numLayers; i++) {
            var layer = comp.layer(i);
            replaceExpressionsInLayer(layer);
        }

        app.endUndoGroup(); // 실행 취소 그룹 종료
    }

    function replaceExpressionsInLayer(layer) {
        var properties = getAllProperties(layer);

        for (var i = 0; i < properties.length; i++) {
            var prop = properties[i];

            if (prop.canSetExpression && prop.expressionEnabled) {
                var expr = prop.expression;
                var newExpr = expr.replace(/슬라이더/g, "Slider");

                if (expr !== newExpr) {
                    prop.expression = newExpr;
                }
            }
        }
    }

    function getAllProperties(group, properties) {
        properties = properties || [];

        if (group.numProperties) {
            for (var i = 1; i <= group.numProperties; i++) {
                var prop = group.property(i);
                properties.push(prop);
                if (prop instanceof PropertyGroup || prop instanceof MaskPropertyGroup) {
                    getAllProperties(prop, properties);
                }
            }
        }

        return properties;
    }

    replaceSliderExpressions();
}
