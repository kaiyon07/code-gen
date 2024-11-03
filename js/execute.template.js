import _ from 'lodash';
import inputs from './inputs.json' assert { type: 'json' };

function test() {
    let originalResults = Array();
    let optimizedResults = Array();
    let refactoredResults = Array();

    let runtimeOriginal = 0;
    {
        // #put ORIGINAL

        let testInputs = JSON.parse(JSON.stringify(inputs.testInputs));
        let t0 = performance.now();
        testInputs.forEach(
            (input) => {
                try {
                    originalResults.push(eval(`${inputs.functionName}(...input)`))
                }
                catch (e) {
                    originalResults.push(typeof e)
                }
            }
        );
        let t1 = performance.now();
        runtimeOriginal = t1 - t0;

        // Check for exceptions
        let testInputs2 = JSON.parse(JSON.stringify(inputs.testInputs));
        let numErrors = 0;
        testInputs2.forEach(
            (input) => {
                try {
                    eval(`${inputs.functionName}(...input)`)
                }
                catch (e) {
                    numErrors++;
                }
            }
        );

        if (numErrors === inputs.testInputs.length)
        {
            console.log(JSON.stringify({
                evaluationError: "Original code does not run properly, all tests return error"
            }));
            return;
        }
    }

    // reset variable name if the name is put in VariableEnvironment through use of var
    try {
        eval(`${inputs.functionName} = null`)
    } catch { }

    let runtimeOptimized = 0;
    {
        // #put OPTIMIZED

        let testInputs = JSON.parse(JSON.stringify(inputs.testInputs));
        let t0 = performance.now();
        testInputs.forEach(
            (input) => {
                try {
                    optimizedResults.push(eval(`${inputs.functionName}(...input)`))
                }
                catch (e) {
                    optimizedResults.push(typeof e)
                }
            }
        )
        let t1 = performance.now();
        runtimeOptimized = t1 - t0;
    }

    let runtimeRefactored = 0;
    {
        // #put REFACTORED

        let testInputs = JSON.parse(JSON.stringify(inputs.testInputs));
        let t0 = performance.now();
        testInputs.forEach(
            (input) => {
                try {
                    refactoredResults.push(eval(`${inputs.functionName}(...input)`))
                }
                catch (e) {
                    refactoredResults.push(typeof e)
                }
            }
        )
        let t1 = performance.now();
        runtimeRefactored = t1 - t0;
    }

    if (originalResults.length !== refactoredResults.length)
    {
        console.log(JSON.stringify({
            evaluationError: "Original length != refactored length"
        }));
        return;
    }

    if (originalResults.length !== optimizedResults.length)
    {
        console.log(JSON.stringify({
            evaluationError: "Original length != optimized length"
        }));
        return;
    }

    let numOptimizedCorrect = 0;
    let numRefactoredCorrect = 0;
    originalResults.forEach(
        (exp, i) => {
            console.log(`${exp} ${refactoredResults[i]} ${optimizedResults[i]}`);
            if (_.isEqual(exp, refactoredResults[i]))
                numRefactoredCorrect++;

            if (_.isEqual(exp, optimizedResults[i]))
                numOptimizedCorrect++;
        }
    )

    console.log(JSON.stringify({
        runtimeOriginal: runtimeOriginal,
        runtimeOptimized: runtimeOptimized,
        runtimeRefactored: runtimeRefactored,
        numOptimizedCorrect: numOptimizedCorrect,
        numRefactoredCorrect: numRefactoredCorrect,
        total: originalResults.length
    }));
}

try {
    test();
}
catch (e) {
    console.log(JSON.stringify({
        evaluationError: e
    }));
}
